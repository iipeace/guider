<template>
  <footer class="footer">
    <div class="container-fluid">
      <ul class="nav">
        <li class="nav-item">
          <a class="nav-link" href="http://www.creative-tim.com">
            Creative Tim
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="http://blog.creative-tim.com">
            Blog
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="http://www.creative-tim.com/license">
            Licenses
          </a>
        </li>
      </ul>
      <div class="copyright">
        © {{year}} made with <i class="tim-icons icon-heart-2"></i> by
        <a href="https://www.binarcode.com" target="_blank" rel="noopener">Binar Code</a>&nbsp;&
        <a href="https://www.creative-tim.com" target="_blank" rel="noopener">Creative Tim</a> for a better web.
      </div>
    </div>
  </footer>
</template>
<script>
  export default {
    data() {
      return {
        year: new Date().getFullYear()
      }
    }
  };
</script>
<style>
</style>
