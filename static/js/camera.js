document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video-preview');
    const canvas = document.getElementById('canvas');
    const startBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-btn');
    const cameraForm = document.getElementById('camera-form');
    const cameraInput = document.getElementById('camera-image-input');
    let stream = null;

    startBtn.addEventListener('click', async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            startBtn.style.display = 'none';
            captureBtn.style.display = 'block';
        } catch (err) {
            console.error("Error accessing camera: ", err);
            alert("Could not access camera. Please make sure you have allowed camera permissions.");
        }
    });

    captureBtn.addEventListener('click', () => {
        if (!stream) return;

        // Set canvas dimensions to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw video frame to canvas
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convert to base64
        const dataUrl = canvas.toDataURL('image/jpeg');
        cameraInput.value = dataUrl;
        
        // Stop stream
        stream.getTracks().forEach(track => track.stop());
        
        // Submit form
        cameraForm.submit();
    });
});
