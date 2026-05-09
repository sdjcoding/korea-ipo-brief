# 韩国 KOSDAQ 上市机会简报

一个面向中国 AI 录音笔/AI 硬件公司的中文单页 pitch，可发链接到手机阅读。

> **核心信息**：2026 起 KOSDAQ「技术特례上市」正式扩展至 AI 行业；中国 AI 硬件公司在 ARR $20–80M 区间走「技术特례 + 韩国本地实体」路径，估值锚定 $200M – $1.5B。

## 文件结构

```
.
├── index.html           # 主页面（11 个 section + 11 节 CTA + 页脚）
├── assets/
│   ├── favicon.svg      # 站点图标
│   ├── og-image.png     # 链接预览卡片（1200x630，微信/Telegram/Slack 通用）
│   ├── og-image.svg     # 矢量备份（原始设计）
│   └── _generate_og.py  # 重新生成 PNG 的脚本（修改文案后跑 `python3 assets/_generate_og.py`）
├── .nojekyll            # 关闭 GitHub Pages Jekyll 处理
└── README.md            # 本文件
```

## 发送给客户前 — 必做的两步编辑

打开 `index.html`，搜索 `用户编辑区`：

1. **第 11 节 CTA 二维码**（行内注释 `用户编辑区 #1`）：把 `[二维码占位]` 占位 div 替换为你的微信二维码 `<img>`。例如：
   ```html
   <img src="./assets/wechat-qr.png" alt="微信二维码" class="aspect-square max-w-[160px] mx-auto rounded-lg" />
   ```
   把二维码图片放到 `assets/wechat-qr.png`。

2. **第 11 节 CTA 邮箱**（行内注释 `用户编辑区 #2`）：把 `[your-email@example.com]` 替换为你的真实邮箱。

可选：
- 顶部 `<title>` 与 OG meta description 也可替换为更个性化的措辞。
- 页脚 © 行可以加你的姓名/品牌。

## 本地预览

```bash
cd "/Users/dj-mbpm3max/Library/CloudStorage/Dropbox/Claude Code Dropbox/KOREA IPO AI"
python3 -m http.server 8000
```

浏览器打开 `http://localhost:8000`。

**手机真机测试**：手机连同一 WiFi，访问 `http://<电脑局域网IP>:8000`。
（电脑 IP 用 `ipconfig getifaddr en0` 查。）

## 部署到 GitHub Pages（5 分钟）

1. 在 GitHub 创建一个 public repo，建议名 `korea-ipo-brief`。
2. 把本目录所有文件 push 到 `main`：
   ```bash
   git init
   git add .
   git commit -m "韩国 KOSDAQ 上市机会简报 v1"
   git branch -M main
   git remote add origin https://github.com/<你的用户名>/korea-ipo-brief.git
   git push -u origin main
   ```
3. GitHub repo → **Settings → Pages → Source: `Deploy from a branch` → Branch: `main` / `/ (root)`** → Save。
4. 等 1-2 分钟，URL 变绿后访问：
   ```
   https://<你的用户名>.github.io/korea-ipo-brief/
   ```
5. 用手机打开该 URL 验证移动端显示。

## 发链接给客户的建议

- 微信/Telegram/Slack 发链接时会抓取 OG 卡片（`assets/og-image.png`，1200×630，91KB）。微信对 SVG OG 图支持不稳定，所以默认用 PNG。
- 如果你修改了 hero 区域文案、想让 OG 卡片同步更新：编辑 `assets/_generate_og.py` 顶部文字部分，然后跑 `python3 assets/_generate_og.py` 重新生成。
- 简报全部异步加载、首屏 < 1MB，3G 网络也能秒开。
- 客户侧若打开为简体中文乱码：极少数老旧 Android 浏览器会发生，可让对方换用 Chrome/微信内置浏览器。

## 内容更新

文档结构清晰，每个 section 用 HTML 注释标注（`<!-- ===== N. SECTION NAME ===== -->`），直接搜索章节名修改即可。

数据源（行内 `<sup>` 角标 + 页脚汇总）截至 2025-09 / 2026-02 公开数据。如需更新某条数据，搜索原始数字（如 `$250M`、`857 万`）替换。

## 法律免责

本简报为前期市场研究与 IPO 路径概览，**不构成投资建议、法律意见或任何形式的承销承诺**。具体上市方案需基于贵公司实际情况，由持牌专业机构正式评估。
