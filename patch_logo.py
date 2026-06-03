import glob
import os

def patch_templates():
    # Login.html has a specific inline style
    login_path = "templates/login.html"
    if os.path.exists(login_path):
        with open(login_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        old_login_logo = '<div class="brand-logo" style="display: inline-block; width: 48px; height: 48px; background: var(--primary); color: white; border-radius: 12px; font-weight: 700; font-size: 1.5rem; line-height: 48px; margin-bottom: 1rem;">S</div>'
        new_login_logo = '<img src="/static/scrapk.webp" alt="ScrapK Logo" style="display: inline-block; width: 64px; height: 64px; border-radius: 12px; object-fit: cover; margin-bottom: 1rem;">'
        
        if old_login_logo in content:
            content = content.replace(old_login_logo, new_login_logo)
            with open(login_path, "w", encoding="utf-8") as f:
                f.write(content)
                print(f"Patched {login_path}")

    # Other templates use the sidebar structure
    old_logo = '<div class="brand-logo">S</div>'
    new_logo = '<img src="/static/scrapk.webp" alt="ScrapK Logo" class="brand-logo" style="width: 32px; height: 32px; border-radius: 8px; object-fit: cover; background: none; border: none; padding: 0;">'
    
    for filepath in glob.glob("templates/*.html"):
        if filepath.endswith("login.html"):
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if old_logo in content:
            content = content.replace(old_logo, new_logo)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
                print(f"Patched {filepath}")

if __name__ == "__main__":
    patch_templates()
