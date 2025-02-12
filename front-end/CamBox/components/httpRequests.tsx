export const switchCamera = async (direction: string) => {
    try {
        const response = await fetch("http://192.168.113.92:5000/switchCamera", { // get .env to work here
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({camera: direction}),
        });
        const result = await response.json();
        console.log("Response:", result);
      
    } catch (error) {
        console.error("Error switching camera:", error);
    }
}

