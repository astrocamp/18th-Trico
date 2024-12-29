<template>
    <div id="app">
      <h1>{{ message }}</h1>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        message: 'Hello from Vue 3 with Esbuild!',
      };
    },
  };
  </script>
  
  <style>
  h1 {
    color: blue;
  }
  </style>
  