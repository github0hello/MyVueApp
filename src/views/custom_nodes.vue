<template>
  <el-autocomplete
    v-model="state2"
    :fetch-suggestions="querySearch"
    :trigger-on-focus="false"
    clearable
    class="inline-input w-50"
    placeholder="搜索节点名称..."
    @select="handleSelect"
  />
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const state2 = ref('');
const restaurants = ref([]);

const querySearch = (queryString, cb) => {
  const results = queryString
    ? restaurants.value.filter(createFilter(queryString))
    : restaurants.value;
  cb(results);
};

const createFilter = (queryString) => {
  return (restaurant) => {
    return (
      restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    );
  };
};

const handleSelect = (item) => {
  console.log(item);
};

onMounted(() => {
  axios.get('http://127.0.0.1:8080/get_node_list')
    .then(response => {
      // 将返回的节点列表转换为autocomplete需要的格式
      const nodes = response.data.split(';');
      restaurants.value = nodes.map(node => ({ value: node.trim() }));
    })
    .catch(error => {
      console.error('Error fetching node list:', error);
    });
});
</script>
