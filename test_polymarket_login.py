#!/usr/bin/env python3
"""
Polymarket 登录测试
使用 Playwright 无头浏览器
"""

import sys
sys.path.insert(0, '/home/angeless_wanganqi/.venv/polymarket/lib/python3.13/site-packages')

from playwright.sync_api import sync_playwright
import time

EMAIL = "deki.angel.partner@gmail.com"
PASSWORD = "Dk!p4rtN3r$2026xQ"

def login_polymarket():
    with sync_playwright() as p:
        # 启动无头浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        try:
            print("🌐 访问 Polymarket...")
            page.goto("https://polymarket.com", wait_until="networkidle")
            time.sleep(2)
            
            # 截图首页
            page.screenshot(path="polymarket_homepage.png")
            print("✅ 首页截图保存: polymarket_homepage.png")
            
            # 查找登录按钮
            login_btn = page.locator("button:has-text('Connect'), button:has-text('Sign In'), text='Sign In'").first
            if login_btn.count() > 0:
                print("🔐 发现登录按钮，尝试点击...")
                login_btn.click()
                time.sleep(2)
                
                # 查找 Google 登录
                google_btn = page.locator("text=Google, button:has-text('Google')").first
                if google_btn.count() > 0:
                    print("🔑 使用 Google 登录...")
                    google_btn.click()
                    time.sleep(3)
                    
                    # 输入邮箱
                    page.fill("input[type='email']", EMAIL)
                    page.click("button:has-text('Next'), #identifierNext")
                    time.sleep(2)
                    
                    # 输入密码
                    page.fill("input[type='password']", PASSWORD)
                    page.click("button:has-text('Next'), #passwordNext")
                    time.sleep(5)
                    
                    print("✅ 登录信息已提交")
                else:
                    print("⚠️ 未发现 Google 登录选项")
            else:
                print("ℹ️ 可能已登录或无需登录")
            
            # 等待页面加载
            time.sleep(5)
            
            # 截图登录后页面
            page.screenshot(path="polymarket_logged_in.png")
            print("✅ 登录后截图保存: polymarket_logged_in.png")
            
            # 获取页面内容
            content = page.content()
            with open("polymarket_page.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("✅ 页面内容保存: polymarket_page.html")
            
            # 尝试提取市场数据
            markets = extract_markets(page)
            
            browser.close()
            return markets
            
        except Exception as e:
            print(f"❌ 错误: {e}")
            page.screenshot(path="polymarket_error.png")
            browser.close()
            return []

def extract_markets(page):
    """提取市场数据"""
    markets = []
    
    # 尝试多种选择器
    selectors = [
        "[data-testid='market-card']",
        ".market-card",
        "a[href*='/market']",
        ".EventCard"
    ]
    
    for selector in selectors:
        cards = page.locator(selector).all()
        if cards:
            print(f"✅ 找到 {len(cards)} 个市场卡片 (选择器: {selector})")
            for i, card in enumerate(cards[:10]):
                try:
                    text = card.inner_text()
                    markets.append({"index": i+1, "text": text[:200]})
                except:
                    pass
            break
    
    if not markets:
        print("⚠️ 未找到市场卡片，可能需要登录")
    
    return markets

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Polymarket 登录测试")
    print("=" * 50)
    print()
    
    markets = login_polymarket()
    
    print()
    print("=" * 50)
    if markets:
        print(f"✅ 成功提取 {len(markets)} 个市场")
        for m in markets[:5]:
            print(f"  [{m['index']}] {m['text'][:80]}...")
    else:
        print("⚠️ 未提取到市场数据")
        print("请检查截图和 HTML 文件")
    print("=" * 50)
