<div class="playing">
  <div class="rect1" />
  <div class="rect2" />
  <div class="rect3" />
  <div class="rect4" />
  <div class="rect5" />
</div>

<style lang="postcss">
  .playing {
    @apply grid grid-cols-5 w-3.5 h-4 gap-[1px] transition-all ease-in-out;
  }
  .playing > div {
    @apply bg-alice-blue h-full inline-block ease-in-out duration-200 transition-all;
    animation: wavy 1s ease infinite forwards;
    transform-origin: 50% 50%;
  }
  .playing .rect2 {
    animation-delay: 0.25s;
  }
  .playing .rect3 {
    animation-delay: 0.5s;
  }
  .playing .rect4 {
    animation-delay: 0.75s;
  }
  .playing .rect5 {
    animation-delay: 1s;
  }
  @keyframes wavy {
    0% {
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
    50% {
      -webkit-transform: scaleY(0.6);
      transform: scaleY(0.6);
    }
    100% {
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
  }
</style>
