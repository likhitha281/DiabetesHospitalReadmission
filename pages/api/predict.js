/**
 * Next.js API Route - Proxy to Railway Python API
 * 
 * This route proxies requests to the Railway-deployed Python API.
 */

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle OPTIONS request
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Get Railway API URL from environment variable
  const railwayApiUrl = process.env.RAILWAY_API_URL || process.env.NEXT_PUBLIC_API_URL;

  if (!railwayApiUrl) {
    return res.status(503).json({ 
      error: 'Python prediction service not configured',
      message: 'The Python API needs to be deployed to Railway first.',
      stepByStep: {
        step1: 'Go to https://railway.app and sign up with GitHub',
        step2: 'Create new project → Deploy from GitHub → Select your repo',
        step3: 'Set Start Command: python app.py',
        step4: 'Add environment variable MODEL_BASE_URL with your GitHub release URL',
        step5: 'Copy your Railway URL (e.g., https://your-app.railway.app)',
        step6: 'In Vercel Dashboard → Settings → Environment Variables',
        step7: 'Add RAILWAY_API_URL = your Railway URL',
        step8: 'Redeploy Vercel'
      },
      help: 'See QUICK_FIX_API.md or RAILWAY_DEPLOY.md for detailed instructions'
    });
  }

  try {
    // Proxy request to Railway API
    const railwayResponse = await fetch(`${railwayApiUrl}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req.body),
      // Add timeout
      signal: AbortSignal.timeout(30000) // 30 second timeout
    });

    if (!railwayResponse.ok) {
      const errorText = await railwayResponse.text();
      return res.status(railwayResponse.status).json({ 
        error: 'Railway API error',
        message: errorText,
        status: railwayResponse.status
      });
    }

    const data = await railwayResponse.json();
    return res.status(200).json(data);
    
  } catch (error) {
    console.error('Error calling Railway API:', error);
    
    // More specific error messages
    if (error.name === 'AbortError' || error.message.includes('timeout')) {
      return res.status(504).json({ 
        error: 'Request timeout',
        message: 'The Railway API took too long to respond. Check if Railway service is running.',
        hint: 'Go to Railway dashboard and check service status and logs'
      });
    }
    
    if (error.message.includes('ECONNREFUSED') || error.message.includes('fetch failed')) {
      return res.status(503).json({ 
        error: 'Cannot connect to Railway API',
        message: 'The Railway API is not reachable. Check:',
        checks: [
          '1. Railway service is deployed and running',
          '2. RAILWAY_API_URL is correct in Vercel environment variables',
          '3. Railway URL includes https:// (not http://)',
          '4. Railway service is not sleeping (free tier may sleep after inactivity)'
        ],
        railwayUrl: railwayApiUrl
      });
    }
    
    return res.status(500).json({ 
      error: 'Failed to connect to prediction service',
      message: error.message,
      hint: 'Check Railway dashboard for service status and logs'
    });
  }
}
