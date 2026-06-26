import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function main() {
  const imagePath = '/home/z/my-project/upload/pasted_image_1782496128180.png';
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');
  const dataUrl = `data:image/png;base64,${base64Image}`;

  console.log('Image size:', (imageBuffer.length / 1024).toFixed(1), 'KB');
  console.log('Base64 length:', (base64Image.length / 1024).toFixed(1), 'KB');
  console.log('Initializing ZAI...');

  const zai = await ZAI.create();

  console.log('Sending vision request...');

  const response = await zai.chat.completions.createVision({
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: 'Describe this image in detail. What is it? A check, payment confirmation, website screenshot? What text, numbers, dates, names are visible? What is the visual style? Be thorough.',
          },
          {
            type: 'image_url',
            image_url: { url: dataUrl },
          },
        ],
      },
    ],
    thinking: { type: 'disabled' },
  });

  console.log('\n=== VLM ANALYSIS ===\n');
  console.log(response.choices[0]?.message?.content || '(no content)');
  console.log('\n=== END ===\n');
}

main().catch(e => {
  console.error('Error:', e);
  process.exit(1);
});
