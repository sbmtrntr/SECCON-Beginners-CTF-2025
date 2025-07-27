import puppeteer from 'puppeteer';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WEBAPP_URL = process.env.WEBAPP_URL || 'http://web:50000';
const VISIT_TIMEOUT = 10000;

async function visitPost(postId) {
  console.log(`[Bot] Visiting post: ${postId}`);
  
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu'
    ]
  });

  try {
    const page = await browser.newPage();
    
    await page.setCookie({
      name: 'user',
      value: 'admin',
      domain: 'web',
      path: '/'
    });

    const url = `${WEBAPP_URL}/post/${postId}`;
    await page.goto(url, { 
      waitUntil: 'domcontentloaded',
      timeout: VISIT_TIMEOUT 
    });

    await new Promise(resolve => setTimeout(resolve, 3000));
    
    console.log(`[Bot] Successfully visited post: ${postId}`);
    
  } catch (error) {
    console.error(`[Bot] Error visiting post ${postId}:`, error.message);
  } finally {
    await browser.close();
  }
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/') {
    try {
      const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
    } catch (error) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Error loading page');
    }
    return;
  }
  
  if (req.method === 'POST' && req.url === '/visit') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    
    req.on('end', async () => {
      try {
        const { postId } = JSON.parse(body);
        
        if (!postId) {
          res.writeHead(400, { 'Content-Type': 'text/plain' });
          res.end('Missing postId');
          return;
        }
        
        visitPost(postId).catch(console.error);
        
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Visit scheduled');
      } catch (error) {
        res.writeHead(400, { 'Content-Type': 'text/plain' });
        res.end('Invalid request');
      }
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

const PORT = process.env.PORT || 50001;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`[Bot] Admin bot running on port ${PORT}`);
});