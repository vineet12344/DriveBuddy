const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const resultDiv = document.getElementById('result');
const context = canvas.getContext('2d');

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
});

// Capture and send to backend
function capture() {
    context.drawImage(video, 0, 0, 64, 64);
    const imageData = canvas.toDataURL('image/jpeg');

    axios.post('/predict', { image: imageData })
        .then(res => {
            resultDiv.innerText = 'Status: ' + res.data.label;
        })
        .catch(err => console.error(err));
}

