<template>
  <svg
    width="72"
    height="67"
    viewBox="0 0 72 67"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    class="animated-svg"
  >
    <g clip-path="url(#clip0_22_48)">
      <path
        d="M28.38 17.5H23.28V23H28.38V17.5Z"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M47.38 17.5H42.28V23H47.38V17.5Z"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M28.38 28.5H23.28V34H28.38V28.5Z"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M28.38 39.5H23.28V45H28.38V39.5Z"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M28.38 50.5H23.28V56H28.38V50.5Z"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M47.38 28.5H42.28V34H47.38V28.5Z"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M0 65.5H71.44"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M10.88 1.5H59.91"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M10.88 65.5V9.5H59.91V65.5"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M38.7 65.5V41.5H50.6V65.5"
        stroke="#14B8A6"
        stroke-width="3"
        stroke-miterlimit="10"
      />
    </g>
    <defs>
      <clipPath id="clip0_22_48">
        <rect width="71.44" height="67" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
<style>
.animated-svg path {
    stroke-dasharray: 300; /* Ajustar al largo del trazo total */
    stroke-dashoffset: 300; /* Esconde el trazo inicialmente */
    animation: stroke-animation 2s ease-out forwards;
  }

  @keyframes stroke-animation {
    to {
      stroke-dashoffset: 0; /* Revela el trazo */
    }
  }
</style>