/**
 * Next.js API Route - Proxy to Railway Python API
 * 
 * This route proxies requests to the Railway-deployed Python API.
 * If Railway URL is not set, it returns a helpful error message.
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
      message: 'Please deploy the Python API to Railway and set RAILWAY_API_URL environment variable in Vercel.',
      instructions: [
        '1. Deploy app.py to Railway (see RAILWAY_DEPLOY.md)',
        '2. Get your Railway API URL (e.g., https://your-app.railway.app)',
        '3. In Vercel Dashboard → Settings → Environment Variables',
        '4. Add: RAILWAY_API_URL = your Railway URL',
        '5. Redeploy Vercel'
      ],
      help: 'See RAILWAY_DEPLOY.md for detailed instructions'
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
    });

    const data = await railwayResponse.json();
    
    // Return the response with appropriate status
    return res.status(railwayResponse.status).json(data);
    
  } catch (error) {
    console.error('Error calling Railway API:', error);
    return res.status(500).json({ 
      error: 'Failed to connect to prediction service',
      message: error.message,
      hint: 'Make sure Railway API is deployed and RAILWAY_API_URL is correct'
    });
  }
}
