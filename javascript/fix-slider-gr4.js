onUiLoaded(function () {
    // Forge sliders
    document.querySelectorAll('input[type="range"]').forEach((el) => {
        el.className = el.className.replace(/\bsvelte-\S+/g, '').trim();
    });

    // ControlNet Integrated sliders
    document.querySelectorAll('div[class*="range-"]').forEach((el) => {
        el.className = el.className.replace(/\bsvelte-\S+/g, '').trim();
    });

    console.log('[Anxety-Theme]: Svelte classes removed - Forge & CN Integrated Sliders Fixed');
});