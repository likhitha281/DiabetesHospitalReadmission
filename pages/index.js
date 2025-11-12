import { useState } from 'react';
import Head from 'next/head';

export default function Home() {
  const [formData, setFormData] = useState({
    // Numeric features
    time_in_hospital: 3,
    num_lab_procedures: 43,
    num_procedures: 0,
    num_medications: 16,
    number_outpatient: 0,
    number_emergency: 0,
    number_inpatient: 0,
    number_diagnoses: 9,
    
    // Categorical features
    race: 'Caucasian',
    gender: 'Female',
    age: '[50-60)',
    admission_type_id: 1,
    discharge_disposition_id: 1,
    admission_source_id: 7,
    max_glu_serum: 'None',
    A1Cresult: 'None',
    diabetesMed: 'No',
    
    // Medication features
    metformin: 'No',
    repaglinide: 'No',
    nateglinide: 'No',
    glimepiride: 'No',
    glipizide: 'No',
    glyburide: 'No',
    pioglitazone: 'No',
    rosiglitazone: 'No',
    insulin: 'No'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Call the API endpoint
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: formData }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || data.message || 'Prediction failed');
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const clusterColors = {
    0: '#ffcccc',
    1: '#ccffcc',
    2: '#ccccff',
    3: '#ffffcc'
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f5f5f5', padding: '2rem' }}>
      <Head>
        <title>Patient Cluster Predictor | Diabetes Readmission</title>
        <meta name="description" content="Interactive dashboard to predict patient clusters" />
      </Head>

      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        <h1 style={{ 
          textAlign: 'center', 
          fontSize: '2.5rem', 
          color: '#1f77b4', 
          marginBottom: '1rem',
          fontWeight: 'bold'
        }}>
          🏥 Patient Cluster Predictor
        </h1>
        
        <p style={{ 
          textAlign: 'center', 
          fontSize: '1.2rem', 
          color: '#666', 
          marginBottom: '3rem' 
        }}>
          Enter patient information to predict which cluster they belong to
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(3, 1fr)', 
            gap: '2rem',
            marginBottom: '2rem'
          }}>
            {/* Numeric Features Column */}
            <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
              <h2 style={{ marginTop: 0, marginBottom: '1.5rem', color: '#333' }}>📊 Numeric Features</h2>
              
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Time in Hospital (days)
                </label>
                <input
                  type="number"
                  min="1"
                  max="14"
                  value={formData.time_in_hospital}
                  onChange={(e) => handleInputChange('time_in_hospital', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Number of Lab Procedures
                </label>
                <input
                  type="number"
                  min="0"
                  max="200"
                  value={formData.num_lab_procedures}
                  onChange={(e) => handleInputChange('num_lab_procedures', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Number of Procedures
                </label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  value={formData.num_procedures}
                  onChange={(e) => handleInputChange('num_procedures', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Number of Medications
                </label>
                <input
                  type="number"
                  min="0"
                  max="50"
                  value={formData.num_medications}
                  onChange={(e) => handleInputChange('num_medications', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Number of Outpatient Visits
                </label>
                <input
                  type="number"
                  min="0"
                  max="50"
                  value={formData.number_outpatient}
                  onChange={(e) => handleInputChange('number_outpatient', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Number of Emergency Visits
                </label>
                <input
                  type="number"
                  min="0"
                  max="50"
                  value={formData.number_emergency}
                  onChange={(e) => handleInputChange('number_emergency', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Number of Inpatient Visits
                </label>
                <input
                  type="number"
                  min="0"
                  max="50"
                  value={formData.number_inpatient}
                  onChange={(e) => handleInputChange('number_inpatient', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Number of Diagnoses
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={formData.number_diagnoses}
                  onChange={(e) => handleInputChange('number_diagnoses', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>
            </div>

            {/* Categorical Features Column */}
            <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
              <h2 style={{ marginTop: 0, marginBottom: '1.5rem', color: '#333' }}>📋 Categorical Features</h2>
              
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Race</label>
                <select
                  value={formData.race}
                  onChange={(e) => handleInputChange('race', e.target.value)}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                >
                  <option value="Caucasian">Caucasian</option>
                  <option value="AfricanAmerican">AfricanAmerican</option>
                  <option value="Asian">Asian</option>
                  <option value="Hispanic">Hispanic</option>
                  <option value="Other">Other</option>
                  <option value="?">Unknown</option>
                </select>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Gender</label>
                <select
                  value={formData.gender}
                  onChange={(e) => handleInputChange('gender', e.target.value)}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                >
                  <option value="Female">Female</option>
                  <option value="Male">Male</option>
                  <option value="Unknown/Invalid">Unknown/Invalid</option>
                </select>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Age Group</label>
                <select
                  value={formData.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                >
                  <option value="[0-10)">0-10</option>
                  <option value="[10-20)">10-20</option>
                  <option value="[20-30)">20-30</option>
                  <option value="[30-40)">30-40</option>
                  <option value="[40-50)">40-50</option>
                  <option value="[50-60)">50-60</option>
                  <option value="[60-70)">60-70</option>
                  <option value="[70-80)">70-80</option>
                  <option value="[80-90)">80-90</option>
                  <option value="[90-100)">90-100</option>
                </select>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Admission Type ID</label>
                <input
                  type="number"
                  min="1"
                  max="9"
                  value={formData.admission_type_id}
                  onChange={(e) => handleInputChange('admission_type_id', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Discharge Disposition ID</label>
                <input
                  type="number"
                  min="1"
                  max="30"
                  value={formData.discharge_disposition_id}
                  onChange={(e) => handleInputChange('discharge_disposition_id', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Admission Source ID</label>
                <input
                  type="number"
                  min="1"
                  max="25"
                  value={formData.admission_source_id}
                  onChange={(e) => handleInputChange('admission_source_id', parseInt(e.target.value))}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Max Glucose Serum</label>
                <select
                  value={formData.max_glu_serum}
                  onChange={(e) => handleInputChange('max_glu_serum', e.target.value)}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                >
                  <option value="None">None</option>
                  <option value="Norm">Norm</option>
                  <option value=">200">Greater than 200</option>
                  <option value=">300">Greater than 300</option>
                </select>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>A1C Result</label>
                <select
                  value={formData.A1Cresult}
                  onChange={(e) => handleInputChange('A1Cresult', e.target.value)}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                >
                  <option value="None">None</option>
                  <option value="Norm">Norm</option>
                  <option value=">7">Greater than 7</option>
                  <option value=">8">Greater than 8</option>
                </select>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Diabetes Medication</label>
                <select
                  value={formData.diabetesMed}
                  onChange={(e) => handleInputChange('diabetesMed', e.target.value)}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                  required
                >
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>

            {/* Medication Features Column */}
            <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
              <h2 style={{ marginTop: 0, marginBottom: '1.5rem', color: '#333' }}>💊 Medication Features</h2>
              
              {['metformin', 'repaglinide', 'nateglinide', 'glimepiride', 'glipizide', 'glyburide', 'pioglitazone', 'rosiglitazone', 'insulin'].map((med) => (
                <div key={med} style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                    {med.charAt(0).toUpperCase() + med.slice(1).replace('_', ' ')}
                  </label>
                  <select
                    value={formData[med]}
                    onChange={(e) => handleInputChange(med, e.target.value)}
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd' }}
                    required
                  >
                    <option value="No">No</option>
                    <option value="Steady">Steady</option>
                    <option value="Up">Up</option>
                    <option value="Down">Down</option>
                  </select>
                </div>
              ))}
            </div>
          </div>

          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <button
              type="submit"
              disabled={loading}
              style={{
                backgroundColor: loading ? '#ccc' : '#1f77b4',
                color: 'white',
                padding: '1rem 3rem',
                fontSize: '1.2rem',
                border: 'none',
                borderRadius: '8px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontWeight: 'bold',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
              }}
            >
              {loading ? '⏳ Predicting...' : '🔮 Predict Cluster'}
            </button>
          </div>
        </form>

        {error && (
          <div style={{
            backgroundColor: '#fee',
            color: '#c33',
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '2rem',
            border: '1px solid #fcc'
          }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <div style={{
            backgroundColor: 'white',
            padding: '2rem',
            borderRadius: '8px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
            marginTop: '2rem'
          }}>
            <h2 style={{ textAlign: 'center', marginTop: 0, marginBottom: '2rem' }}>🎯 Cluster Prediction Result</h2>
            
            <div style={{
              backgroundColor: clusterColors[result.cluster] || '#f0f0f0',
              padding: '2rem',
              borderRadius: '10px',
              textAlign: 'center',
              marginBottom: '2rem'
            }}>
              <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#1f77b4' }}>
                Cluster {result.cluster}
              </div>
            </div>

            {result.cluster_info && (
              <div>
                <h3 style={{ marginTop: '2rem' }}>📊 Cluster Characteristics</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginTop: '1rem' }}>
                  <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                    <strong>Cluster Size:</strong> {result.cluster_info.size?.toLocaleString() || 'N/A'} patients
                  </div>
                  <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                    <strong>Percentage:</strong> {result.cluster_info.percentage?.toFixed(2) || 'N/A'}%
                  </div>
                </div>

                {result.cluster_info.numeric_means && (
                  <div style={{ marginTop: '2rem' }}>
                    <h3>📈 Average Feature Values</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginTop: '1rem' }}>
                      {Object.entries(result.cluster_info.numeric_means).map(([key, value]) => (
                        <div key={key} style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                          <div style={{ fontWeight: '500', marginBottom: '0.5rem' }}>
                            {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </div>
                          <div style={{ fontSize: '1.2rem', color: '#1f77b4' }}>
                            {typeof value === 'number' ? value.toFixed(2) : value}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {result.cluster_info.readmission_dist && Object.keys(result.cluster_info.readmission_dist).length > 0 && (
                  <div style={{ marginTop: '2rem' }}>
                    <h3>📉 Readmission Distribution</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginTop: '1rem' }}>
                      {Object.entries(result.cluster_info.readmission_dist).map(([key, value]) => (
                        <div key={key} style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                          <div style={{ fontWeight: '500' }}>{key}</div>
                          <div style={{ fontSize: '1.2rem', color: '#1f77b4' }}>
                            {(value * 100).toFixed(1)}%
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
