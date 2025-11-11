import Head from 'next/head'

export default function Home() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <Head>
        <title>Diabetes Readmission Analysis</title>
      </Head>
      
      <h1>Diabetes Hospital Readmission - Clustering Analysis</h1>
      
      <div style={{ marginTop: '2rem' }}>
        <h2>About This Project</h2>
        <p>
          This dashboard displays the results from the clustering and dimensionality 
          reduction analysis performed on the diabetes hospital readmission dataset.
        </p>
        
        <h3>Analysis Components:</h3>
        <ul>
          <li>K-Means Clustering</li>
          <li>Hierarchical Clustering</li>
          <li>DBSCAN Clustering</li>
          <li>PCA Dimensionality Reduction</li>
          <li>t-SNE Visualization</li>
          <li>UMAP Visualization</li>
        </ul>
        
        <div style={{ marginTop: '2rem', padding: '1rem', background: '#f0f0f0', borderRadius: '8px' }}>
          <p><strong>Note:</strong> To display your actual analysis results:</p>
          <ol>
            <li>Export visualizations from your Jupyter notebook as images</li>
            <li>Save cluster results as JSON/CSV files</li>
            <li>Import and display them in this Next.js app</li>
            <li>Or create API routes to serve the data dynamically</li>
          </ol>
        </div>
      </div>
    </div>
  )
}

