export function useOnClickOutside(rootEl, callback) {
	// `mousedown` or `mouseup` is better than `click` here because it doesn't bubble up like `click`
	// if you've used `click` here, the callback will be run immediatly.
    window.addEventListener('click', e => {
		const clickedEl = e.target

		// skip if the root element contains the clicked element
		if (rootEl?.contains(clickedEl)) {
			return
		}
		// otherwise execute the action
		callback()
	})
}
