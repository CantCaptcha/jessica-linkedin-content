const fs = require('fs');
const { mdToPdf } = require('markdown-to-pdf');

// Read the markdown file
const mdContent = fs.readFileSync('docs/BACKUP-GUIDE.md', 'utf8');

// Create PDF
mdToPdf(mdContent)
    .then(pdfBuffer => {
        fs.writeFileSync('docs/BACKUP-GUIDE.pdf', pdfBuffer);
        console.log('✅ PDF created: docs/BACKUP-GUIDE.pdf');
    })
    .catch(err => {
        console.error('❌ Error creating PDF:', err);
        process.exit(1);
    });
