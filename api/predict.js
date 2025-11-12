/**
 * Vercel Serverless Function Wrapper for Python Prediction API
 * This is a Node.js wrapper that calls the Python function
 * 
 * Note: For direct Python execution, Vercel requires the function to be in api/predict.py
 * This JS file serves as a fallback or can be used to call external Python services
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

  try {
    // For Vercel, Python functions are handled separately
    // This is a placeholder - the actual Python function should be in api/predict.py
    // If you need to use this JS version, you'd need to set up an external Python service
    
    return res.status(501).json({ 
      error: 'Python prediction endpoint not available',
      message: 'Please ensure api/predict.py is properly configured for Vercel Python runtime'
    });
  } catch (error) {
    return res.status(500).json({ 
      error: 'Server error',
      message: error.message 
    });
  }
}

