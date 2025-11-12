/**
 * Next.js API Route that proxies to Python serverless function
 * In Vercel, this will route to api/predict.py based on vercel.json configuration
 * This provides a fallback if Python function is not available
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

  // In Vercel, the route /api/predict is configured to use api/predict.py
  // So this Next.js route should not be called, but serves as a fallback
  // If you reach here, it means the Python function might not be available
  
  return res.status(503).json({ 
    error: 'Python prediction service not available',
    message: 'Please ensure api/predict.py is properly configured for Vercel Python runtime'
  });
}

