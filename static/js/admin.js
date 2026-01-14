function addProduct() {
    const data = {
        barcode: document.getElementById("barcode").value,
        product_name: document.getElementById("name").value,
        brand: document.getElementById("brand").value,
        manufacturing_date: document.getElementById("mfg").value,
        expiry_date: document.getElementById("exp").value,
        price: document.getElementById("price").value,
        description: document.getElementById("desc").value
    };

    fetch("/add-product", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        const msg = document.getElementById("msg");

        if (res.status === "success") {
            msg.innerHTML = `<p style="color:green">${res.message}</p>`;
        } else {
            msg.innerHTML = `<p style="color:red">${res.message}</p>`;
        }
    });
}
