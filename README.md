# Diabetes Hospital Readmission - Web Dashboard

This is a Next.js web application that displays the results from the clustering and dimensionality reduction analysis.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Deploy to Vercel:
```bash
vercel
```

## Project Structure

- `pages/index.js` - Main dashboard page
- `ClusteringAndDimensionalityReduction.ipynb` - Original analysis notebook
- `data/` - Dataset files

## Next Steps

To fully integrate your analysis:

1. Export visualizations from the notebook as images
2. Save cluster results as JSON files
3. Create API routes in `pages/api/` to serve data
4. Add visualization components using libraries like Chart.js or D3.js

