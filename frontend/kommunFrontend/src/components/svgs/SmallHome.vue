<template>
  <svg
    width="98"
    height="63"
    viewBox="0 0 98 63"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    class="animated-svg"
  >
    <g clip-path="url(#clip0_22_60)">
      <path
        d="M0 60.8999H98"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M88 26.8999V60.8999"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M7.16 22.76V60.9"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M2 25.8999L33 1.8999L63.56 25.8999H92.87"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M26.29 60.9V39.5H39.4V60.9"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M22.26 26.8999H16.4V34.1999H22.26V26.8999Z"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M36.26 26.8999H30.4V34.1999H36.26V26.8999Z"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M50.26 26.8999H44.4V34.1999H50.26V26.8999Z"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M65.26 36.8999H59.4V44.1999H65.26V36.8999Z"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
      <path
        d="M80.26 36.8999H74.4V44.1999H80.26V36.8999Z"
        stroke="#F97316"
        stroke-width="3"
        stroke-miterlimit="10"
      />
    </g>
    <defs>
      <clipPath id="clip0_22_60">
        <rect width="98" height="62.4" fill="white" />
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
