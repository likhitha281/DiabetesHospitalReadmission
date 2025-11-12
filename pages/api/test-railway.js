/**
 * Test endpoint to check Railway connection
 * Visit: https://your-app.vercel.app/api/test-railway
 */

export default async function handler(req, res) {
  const railwayApiUrl = process.env.RAILWAY_API_URL || process.env.NEXT_PUBLIC_API_URL;
  
  const info = {
    railwayUrlConfigured: !!railwayApiUrl,
    railwayUrl: railwayApiUrl || 'NOT SET',
    environment: process.env.NODE_ENV,
    timestamp: new Date().toISOString()
  };

  if (!railwayApiUrl) {
    return res.status(200).json({
      ...info,
      error: 'RAILWAY_API_URL not set',
      instructions: 'Add RAILWAY_API_URL in Vercel environment variables'
    });
  }

  // Test connection to Railway
  try {
    const healthResponse = await fetch(`${railwayApiUrl}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000)
    });

    if (healthResponse.ok) {
      const healthData = await healthResponse.json();
      return res.status(200).json({
        ...info,
        status: 'SUCCESS',
        railwayHealth: healthData,
        message: 'Railway API is reachable and working!'
      });
    } else {
      return res.status(200).json({
        ...info,
        status: 'ERROR',
        railwayStatus: healthResponse.status,
        message: 'Railway API responded but with an error'
      });
    }
  } catch (error) {
    return res.status(200).json({
      ...info,
      status: 'ERROR',
      error: error.message,
      errorType: error.name,
      message: 'Cannot connect to Railway API',
      troubleshooting: [
        '1. Check Railway dashboard - is service running?',
        '2. Verify Railway URL is correct (should start with https://)',
        '3. Check Railway logs for errors',
        '4. Make sure Railway service is not sleeping (free tier may sleep)',
        '5. Try accessing Railway URL directly in browser: ' + railwayApiUrl + '/health'
      ]
    });
  }
}

