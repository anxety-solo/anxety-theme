onUiLoaded(function () {
    // Remove class from all range inputs
    function removeRangeClass() {
        document.querySelectorAll('input[type="range"]').forEach((input) => {
            input.classList.remove('svelte-pc1gm4');
        });
    }
    removeRangeClass();

    console.log('[Anxety-Theme]: Range input class `svelte-pc1gm4` removed - Forge Slider Fixed.');
});
