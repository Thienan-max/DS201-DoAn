# Script to initialize Git and prepare to push to GitHub

Write-Host "Initializing Git repository..." -ForegroundColor Green
git init

Write-Host "Adding files..." -ForegroundColor Green
git add .

Write-Host "Committing changes..." -ForegroundColor Green
git commit -m "Khởi tạo project và các script xử lý dữ liệu"

Write-Host "`n--- BƯỚC TIẾP THEO ---" -ForegroundColor Yellow
Write-Host "Để đưa code này lên GitHub, bạn cần tạo một repository trống trên GitHub, sau đó chạy 3 lệnh sau trong Terminal:"
Write-Host "`tgit branch -M main"
Write-Host "`tgit remote add origin <URL_CỦA_REPO_GITHUB_CỦA_BẠN>"
Write-Host "`tgit push -u origin main"

Write-Host "`nVí dụ:"
Write-Host "`tgit remote add origin https://github.com/username/ten-repo.git"
