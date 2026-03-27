# Active Projects

## QR Code Generator App (Google Play Store)
**Status:** Active Development (2026-03-27)
**Priority:** High
**GitHub:** https://github.com/CantCaptcha/qr-code-generator

### MVP Features
**Free Tier:**
- Basic QR code generation (URLs, text, WiFi)
- Limited customization (standard colors)
- Watermarked exports
- 7-day scan history

**Paid Tier ($1.99/month):**
- Custom logos, colors, frames
- Unlimited scan history with analytics
- Export in multiple formats (PNG, SVG, PDF)
- Batch generation (up to 50 at once)
- Remove watermark

### Tech Stack
- **Android:** Kotlin + Jetpack Compose
- **QR Library:** ZXing ("Zebra Crossing")
- **Storage:** Room database (local)
- **Backend:** Firebase or Supabase (analytics)

### Revenue Model
- Target: 1,000 users @ $1.99/month
- Potential: $1,990/month recurring

### Development Plan
**Week 1-2:** Basic QR generator (URL, text), custom colors, save/export
- [x] Project setup with Jetpack Compose
- [x] ZXing library integration
- [x] Basic QR generation (URL, text)
- [x] Color customization (4 preset colors)
- [x] Save/export functionality (save to gallery with MediaStore)
- [x] **WiFi QR code support** (SSID, password, security type, hidden network)
- [ ] Testing on multiple devices

**Week 3-4:** Logo embedding, scan tracking backend, basic analytics
- [ ] Logo embedding UI
- [ ] Scan tracking backend
- [ ] Firebase/Supabase setup
- [ ] Analytics dashboard
- [ ] Batch generation UI
- [ ] Monetization UI

**Week 5-6:** Monetization & Polish
- [ ] In-app purchases
- [ ] Free vs paid tier separation
- [ ] Watermarking (free tier)
- [ ] Multiple export formats
- [ ] Release to Play Store

### Next Steps
1. Testing on Android emulator/device
2. Add custom color picker (not just presets)
3. Begin analytics backend design

---

## Future Project Ideas (Backlog)

1. **AI Note/Document Summarizer**
   - Summarize long docs with key points and action items
   - Tech: OpenRouter API
   - Monetization: Free with ads, $2.99/month unlimited

2. **Focus Timer with AI Insights**
   - Pomodoro timer with AI pattern analysis
   - Tech: Local storage + optional AI
   - Monetization: $1.99 one-time

3. **Screen Recorder + AI Transcription**
   - Record screen, instant AI transcript/summary
   - Tech: Android screen recording + Whisper/LLM
   - Monetization: Free 5 min/day, $4.99/month unlimited

4. **API Playground for Mobile**
   - Like Postman for phones, test REST APIs
   - Tech: Retrofit, okhttp, Jetpack
   - Monetization: Free limited, $9.99/year Pro

5. **Log/Prompt Analyzer**
   - Analyze LLM prompts/responses for cost/performance
   - Tech: Similar to OpenClaw analysis
   - Monetization: $4.99/month

6. **Expense Splitter for Freelancers/Contractors**
   - Track shared project expenses, generate invoices
   - Integrations: QuickBooks, Stripe
   - Monetization: Freemium, $9.99/year invoicing
