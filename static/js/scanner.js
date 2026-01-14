let html5QrCode;
let scanTimeout;

function startScanner() {
    document.getElementById("result").innerHTML =
        "<p>📷 Scanning... Please align barcode</p>";

    html5QrCode = new Html5Qrcode("reader");

    Html5Qrcode.getCameras().then(devices => {
        if (!devices || devices.length === 0) {
            alert("No camera found");
            return;
        }

        // 🔥 BACK CAMERA SELECT LOGIC
        let backCamera = devices.find(device =>
            device.label.toLowerCase().includes("back") ||
            device.label.toLowerCase().includes("rear")
        );

        // fallback: last camera (usually back)
        const cameraId = backCamera ? backCamera.id : devices[devices.length - 1].id;

        html5QrCode.start(
            cameraId,
            {
                fps: 5,
                qrbox: { width: 350, height: 120 },
                disableFlip: true,
                formatsToSupport: [
                    Html5QrcodeSupportedFormats.EAN_13,
                    Html5QrcodeSupportedFormats.EAN_8,
                    Html5QrcodeSupportedFormats.CODE_128
                ]
            },
            (decodedText) => {
                clearTimeout(scanTimeout);
                stopScanner();
                scanProduct(decodedText);
            },
            () => {}
        );

        // ⏱️ timeout safety
        scanTimeout = setTimeout(() => {
            stopScanner();
            document.getElementById("result").innerHTML = `
                <h3 style="color:orange">⚠️ No barcode detected</h3>
                <p>Please try again or use manual entry.</p>
            `;
        }, 10000);

    }).catch(err => {
        alert("Camera access error");
        console.error(err);
    });
}

function stopScanner() {
    if (html5QrCode) {
        html5QrCode.stop().then(() => {
            html5QrCode.clear();
        });
    }
}
