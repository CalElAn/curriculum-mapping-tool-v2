<template>
  <div
    class="place-self-center rounded-full bg-contain bg-center bg-no-repeat"
    :style="{
      'background-image': 'url(' + getProfilePictureUrl(profilePicturePath) + ')',
    }"
    alt="profile picture"
  ></div>
</template>

<script setup>
defineProps({
  profilePicturePath: String,
});

function getProfilePictureUrl(profilePicturePath) {
  return `'https://ui-avatars.com/api/?size=40&rounded=true&name=${profilePicturePath}'`;
}
</script>

<style lang="scss" scoped></style>
