function scanProduct(barcode) {
    fetch("/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ barcode: barcode })
    })
    .then(res => res.json())
    .then(data => showResult(data));
}

// Manual input handler
function scanManual() {
    const barcode = document.getElementById("manualBarcode").value;

    if (!barcode) {
        alert("Please enter a barcode");
        return;
    }
    scanProduct(barcode);
}

function showResult(data) {
    const result = document.getElementById("result");

    if (data.status === "success") {
        result.innerHTML = `
            <h3 style="color:green">✔ Verified Product</h3>
            <p><b>Name:</b> ${data.product.name}</p>
            <p><b>Brand:</b> ${data.product.brand}</p>
            <p><b>MFG:</b> ${data.product.mfg}</p>
            <p><b>EXP:</b> ${data.product.exp}</p>
            <p><b>Price:</b> ₹${data.product.price}</p>
            <p><b>Description:</b> ${data.product.description}</p>
        `;
    } else {
        result.innerHTML = `
            <h3 style="color:red">❌ Fake / Unverified Product</h3>
            <p>${data.message}</p>
        `;
    }
}
