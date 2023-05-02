document.addEventListener("DOMContentLoaded", () => {
  console.log("wallet.js loaded");
  const provider = getProvider();

  if (!provider) {
    console.log("Twetch Wallet not found. Please install the extension.");
    return;
  }

  const connectButton = document.getElementById("connect-wallet");
  const makePaymentButtons = document.getElementsByClassName("payment-button");

  connectButton.addEventListener("click", async () => {
    console.log("Connect Wallet button clicked");
    try {
      const resp = await provider.connect();
      console.log("Connected:", resp.publicKey.toString(), resp.paymail.toString());
    } catch (err) {
      console.error("Error connecting wallet:", err);
    }
  });

  async function makePaymentsToUserIds() {
    const images = document.querySelectorAll('img[data-userid]');
    const userIds = [...new Set(Array.from(images).map(img => img.dataset.userid))];
    const outputs = userIds.map(userId => ({
      to: `${userId}@twetch.me`,
      sats: 2180, // You can adjust the sats value accordingly
    }));
  
    // Add the additional payment output to 55@twetch.me
    outputs.push({
      to: '55@twetch.me',
      sats: 4200,
    });
  
    try {
      const response = await provider.abi({
        contract: 'payment',
        outputs
      });
  
      console.log(`Payments to multiple users and 55@twetch.me successful.`, response);
    } catch (error) {
      console.error(`Payments to multiple users and 55@twetch.me failed.`, error);
    }
  }
  
  

  // Add the event listeners for the 'random-images' and 'next-images' buttons
  document.getElementById('random-images').addEventListener('click', makePaymentsToUserIds);
  document.getElementById('next-images').addEventListener('click', makePaymentsToUserIds);
});
