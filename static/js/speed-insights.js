/**
 * Vercel Speed Insights Integration
 * 
 * This script initializes Vercel Speed Insights for performance monitoring.
 * It uses the ES module from CDN to inject the tracking script.
 * 
 * Speed Insights will only track data in production (on Vercel).
 * No data is collected in local development.
 */

// Import and initialize Speed Insights using ES module from CDN
import { injectSpeedInsights } from 'https://cdn.jsdelivr.net/npm/@vercel/speed-insights@2.0.0/dist/index.mjs';

// Initialize Speed Insights
// This will automatically detect the environment and only track in production
injectSpeedInsights();
