onUiLoaded(function () {
    if (opts.at_disable_theme) return;

    // Forge sliders - remove default styling class
    function removeRangeClass() {
        document.querySelectorAll('input[type="range"]').forEach((input) => {
            input.classList.remove('svelte-pc1gm4');
        });
    }

    // ControlNet Integrated sliders - remove default styling class
    function removeCNRangeClass() {
        document.querySelectorAll('input[type="range"], div[class*="range-"]').forEach((el) => {
            el.classList.remove('svelte-17pocne');
        });
    }

    removeRangeClass();
    removeCNRangeClass();

    console.log('[Anxety-Theme]: Range input classes `svelte-pc1gm4`, `svelte-17pocne` removed - Forge & CN Integrated Sliders Fixed');
});