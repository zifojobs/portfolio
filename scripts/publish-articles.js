#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Get today's date in format YYYY-MM-DD (UTC)
const today = new Date().toISOString().split('T')[0];
console.log(`📅 Looking for articles scheduled for ${today}...`);

const blogDir = path.join(process.cwd(), 'src/pages/blog');

// Find all .astro files in the blog directory
const files = fs.readdirSync(blogDir).filter(file => {
  return file.endsWith('.astro') && file !== 'index.astro';
});

let published = false;

files.forEach(file => {
  const filePath = path.join(blogDir, file);
  const content = fs.readFileSync(filePath, 'utf-8');

  // Check if this article is scheduled for today
  if (content.includes(`date: "${today}"`)) {
    console.log(`\n🎯 Found article scheduled for today: ${file}`);

    if (content.includes('draft: true')) {
      console.log('   Removing draft status...');

      // Remove the `draft: true,` line
      const updatedContent = content.replace(/\s*draft:\s*true,?\s*\n/g, '');

      fs.writeFileSync(filePath, updatedContent, 'utf-8');
      console.log(`   ✅ Article published: ${file}`);
      published = true;
    } else {
      console.log('   ℹ️  Article is already published');
    }
  }
});

if (!published) {
  console.log(`\nℹ️  No articles scheduled for ${today}`);
  process.exit(0);
}

// Update blog/index.astro to refresh the article list
console.log('\n🔄 Updating blog index...');
const indexPath = path.join(blogDir, 'index.astro');
const indexContent = fs.readFileSync(indexPath, 'utf-8');

// The index.astro filters draft articles automatically,
// so just re-saving it will work since draft status is removed above
fs.writeFileSync(indexPath, indexContent, 'utf-8');
console.log('✅ Blog index refreshed');

console.log('\n🚀 Articles published successfully!');
