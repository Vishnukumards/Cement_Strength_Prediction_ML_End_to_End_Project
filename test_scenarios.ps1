# Test Scenario 1: High-Strength Concrete
Write-Host "=== TEST 1: High-Strength Concrete ===" -ForegroundColor Yellow
$highStrength = @'
{
  "Cement (component 1)(kg in a m^3 mixture)": 450.0,
  "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 100.0,
  "Fly Ash (component 3)(kg in a m^3 mixture)": 50.0,
  "Water  (component 4)(kg in a m^3 mixture)": 150.0,
  "Superplasticizer (component 5)(kg in a m^3 mixture)": 3.0,
  "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 1000.0,
  "Fine Aggregate (component 7)(kg in a m^3 mixture)": 700.0,
  "Age (day)": 28
}
'@
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $highStrength -ContentType "application/json"

# Test Scenario 2: Standard Concrete
Write-Host "`n=== TEST 2: Standard Concrete ===" -ForegroundColor Yellow
$standard = @'
{
  "Cement (component 1)(kg in a m^3 mixture)": 300.0,
  "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 50.0,
  "Fly Ash (component 3)(kg in a m^3 mixture)": 30.0,
  "Water  (component 4)(kg in a m^3 mixture)": 180.0,
  "Superplasticizer (component 5)(kg in a m^3 mixture)": 1.0,
  "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 1100.0,
  "Fine Aggregate (component 7)(kg in a m^3 mixture)": 750.0,
  "Age (day)": 28
}
'@
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $standard -ContentType "application/json"

# Test Scenario 3: Early Strength (7 days)
Write-Host "`n=== TEST 3: Early Strength (7 days) ===" -ForegroundColor Yellow
$early = @'
{
  "Cement (component 1)(kg in a m^3 mixture)": 400.0,
  "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 0.0,
  "Fly Ash (component 3)(kg in a m^3 mixture)": 0.0,
  "Water  (component 4)(kg in a m^3 mixture)": 170.0,
  "Superplasticizer (component 5)(kg in a m^3 mixture)": 2.0,
  "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 1050.0,
  "Fine Aggregate (component 7)(kg in a m^3 mixture)": 680.0,
  "Age (day)": 7
}
'@
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $early -ContentType "application/json"

# Test Scenario 4: Low Cement Mix (FIXED)
Write-Host "`n=== TEST 4: Low Cement Mix (Fixed) ===" -ForegroundColor Yellow
$lowCement = @'
{
  "Cement (component 1)(kg in a m^3 mixture)": 200.0,
  "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 150.0,
  "Fly Ash (component 3)(kg in a m^3 mixture)": 100.0,
  "Water  (component 4)(kg in a m^3 mixture)": 190.0,
  "Superplasticizer (component 5)(kg in a m^3 mixture)": 0.5,
  "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 1145.0,
  "Fine Aggregate (component 7)(kg in a m^3 mixture)": 800.0,
  "Age (day)": 28
}
'@
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $lowCement -ContentType "application/json"

# Test Scenario 5: Ultra High-Strength
Write-Host "`n=== TEST 5: Ultra High-Strength ===" -ForegroundColor Yellow
$ultraHigh = @'
{
  "Cement (component 1)(kg in a m^3 mixture)": 540.0,
  "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 0.0,
  "Fly Ash (component 3)(kg in a m^3 mixture)": 0.0,
  "Water  (component 4)(kg in a m^3 mixture)": 160.0,
  "Superplasticizer (component 5)(kg in a m^3 mixture)": 3.5,
  "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 1000.0,
  "Fine Aggregate (component 7)(kg in a m^3 mixture)": 650.0,
  "Age (day)": 28
}
'@
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $ultraHigh -ContentType "application/json"