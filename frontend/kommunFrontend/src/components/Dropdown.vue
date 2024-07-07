<template>
		<span ref="root" class="relative inline-block" v-bind="$attrs">
			<div ref="reference" :class="referenceClass">
				<slot
					name="reference"
					:is-open="isOpen"
					:toggle="toggle"
					:open="open"
					:close="close"
				/>
			</div>

			<div 
        v-show="isOpen" 
        ref="content" 
        class="top-0 left-0 fixed mt-1 z-50" 
        :class="contentClass"
      >
				<slot name="content" :is-open="isOpen" :close="close" />
			</div>
		</span>
</template>

<script>
	import { createPopper } from '@popperjs/core'
  import EventBus from '/src/utils/event-bus.js'
	import { useOnClickOutside } from '/src/composables/useOnClickOutside.js'

	//import './dropdown.css'

	export default {
		name: 'DropdownBase',
		// components: {
		// 	OnClickOutside,
		// },
		props: {
			show: {
				type: Boolean,
				default: false,
			},
			placement: {
				type: String,
				default: 'bottom',
			},
			offset: {
				type: Array,
				default: () => [0, 0],
			},
			modifiers: {
				type: Array,
				default: () => [],
			},
			strategy: {
				type: String,
				default: 'absolute',
			},
			referenceClass: {
				type: String,
				default: '',
			},
			contentClass: {
				type: String,
				default: '',
			},
			disabled: {
				type: Boolean,
				default: false,
			},
		},
  emits: ['update:show'],
		data() {
			return {
				isOpen: this.show,
				dropdown: null,
			}
  },
  mounted() { 

    useOnClickOutside(this.$refs.root, () => {
      this.close();
    });
  },
		watch: {
			show(show) {
				this.isOpen = show
			},
			isOpen(isOpen) {
				this.$nextTick(() => {
					isOpen ? this.createDropdown() : this.destroyDropdown()
				})
			},
		},
		beforeMount() {
			EventBus.on('close-tag-dropdown', () => {
				this.isOpen = false
			})

			EventBus.on('close-project-dropdown', () => {
				this.isOpen = false
			})
		},
		updated() {
			if (this.isOpen) {
				this.updateDropdown()
			}
		},
		beforeUnmount() {
			EventBus.off('close-tag-dropdown')
			EventBus.off('close-project-dropdown')

			this.destroyDropdown()
		},
		methods: {
			toggle() {
				if (!this.disabled) {
					this.isOpen = !this.isOpen
				}
			},
			updateShow() {
				this.$emit('update:show', this.isOpen)
			},
			open() {
				if (!this.disabled && !this.isOpen) {
					this.isOpen = true
					this.updateShow()
				}
			},
			close() {
				if (!this.disabled && this.isOpen) {
					this.isOpen = false
					this.updateShow()
				}
			},
			createDropdown() {
				const reference = this.$refs.reference
				const content = this.$refs.content

				this.dropdown = createPopper(reference, content, {
					placement: this.placement,
					strategy: this.strategy,
					modifiers: [
						{
							name: 'offset',
							options: {
								offset: this.offset,
							},
						},
						...this.modifiers,
					],
				})
			},
			updateDropdown() {
				if (this.dropdown) {
					this.dropdown.update()
				}
			},
			destroyDropdown() {
				if (this.dropdown) {
					this.dropdown.destroy()
					this.dropdown = null
				}
			},
  },
  
}
</script>
