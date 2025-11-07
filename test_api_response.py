"""
Test the actual API response to see what accuracy is being returned
"""
import requests
import json
import time
from pathlib import Path

print("="*60)
print("TESTING WEB APP API RESPONSE")
print("="*60)

# First, let's check if there are any existing jobs
try:
    response = requests.get('http://localhost:5000/api/jobs')
    jobs_data = response.json()
    print(f"\nExisting jobs: {len(jobs_data.get('jobs', []))}")
    
    if jobs_data.get('jobs'):
        # Get the most recent completed job
        completed_jobs = [j for j in jobs_data['jobs'] if j['status'] == 'completed']
        if completed_jobs:
            latest_job = completed_jobs[-1]
            job_id = latest_job['job_id']
            
            print(f"\nChecking latest job: {job_id}")
            print(f"Filename: {latest_job['filename']}")
            
            # Get detailed status
            status_response = requests.get(f'http://localhost:5000/status/{job_id}')
            status_data = status_response.json()
            
            print("\n" + "="*60)
            print("API RESPONSE:")
            print("="*60)
            print(json.dumps(status_data, indent=2, default=str))
            
            print("\n" + "="*60)
            print("MODEL ACCURACY CHECK:")
            print("="*60)
            
            if 'best_score' in status_data:
                score = status_data['best_score']
                print(f"✓ best_score found: {score}")
                print(f"  Type: {type(score)}")
                print(f"  Value: {score:.10f}")
                print(f"  Percentage: {score * 100:.2f}%")
                
                if score == 0.0:
                    print("\n❌ ERROR: Accuracy IS 0.0000!")
                    print("This is the bug we need to fix!")
                else:
                    print(f"\n✅ SUCCESS: Accuracy is {score * 100:.2f}%")
            else:
                print("❌ ERROR: 'best_score' not found in API response!")
                print("Available keys:", list(status_data.keys()))
        else:
            print("\n⚠️ No completed jobs found. Please run an analysis first.")
    else:
        print("\n⚠️ No jobs found. Please upload a file and run analysis first.")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to web server!")
    print("Make sure the web server is running on http://localhost:5000")
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
