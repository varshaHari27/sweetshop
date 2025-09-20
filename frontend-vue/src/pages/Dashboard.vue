<template>
  <div class="dashboard">
    <!-- Page Title -->
    <h1 class="page-title">Available Sweets</h1>

    <!-- Search bar -->
    <div class="search-bar">
      <input
        type="text"
        v-model="search"
        placeholder="Search for sweets..."
        class="search-input"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">Loading sweets...</div>

    <!-- Sweets Grid -->
    <div class="sweets-grid" v-else>
      <div
        v-for="sweet in filteredSweets"
        :key="sweet.id"
        class="sweet-card"
      >
        <!-- Sweet Image -->
        <div class="image-container">
          <img :src="sweet.image" :alt="sweet.name" class="sweet-image" />
        </div>

        <!-- Sweet Info -->
        <h2 class="sweet-title">{{ sweet.name }}</h2>
        <p class="sweet-description">{{ sweet.description }}</p>
        <p class="sweet-price">₹{{ sweet.price }}</p>
        <p
          :class="['sweet-qty', sweet.quantity === 0 ? 'out-of-stock' : 'in-stock']"
        >
          {{ sweet.quantity === 0 ? "Out of Stock" : "In Stock: " + sweet.quantity }}
        </p>
        <button
          class="purchase-btn"
          :disabled="sweet.quantity === 0 || purchasing[sweet.id]"
          @click="purchaseSweet(sweet.id)"
        >
          {{ purchasing[sweet.id] ? "Purchasing..." : "Purchase" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../api.js";

const sweets = ref([]);
const search = ref("");
const loading = ref(false);
const purchasing = ref({}); // track which sweet is being purchased

const fetchSweets = async () => {
  loading.value = true;
  try {
    const response = await api.get("/sweets");
    sweets.value = response.data;
  } catch (error) {
    console.error("Error fetching sweets:", error);
  } finally {
    loading.value = false;
  }
};

const purchaseSweet = async (sweetId) => {
  purchasing.value[sweetId] = true;
  try {
    await api.post(`/sweets/${sweetId}/purchase`);
    // update quantity locally
    const sweet = sweets.value.find((s) => s.id === sweetId);
    if (sweet) sweet.quantity -= 1;
  } catch (error) {
    console.error("Purchase failed:", error);
    alert(error.response?.data?.detail || "Purchase failed");
  } finally {
    purchasing.value[sweetId] = false;
  }
};

onMounted(() => {
  fetchSweets();
});

const filteredSweets = computed(() =>
  sweets.value.filter((sweet) =>
    sweet.name.toLowerCase().includes(search.value.toLowerCase())
  )
);
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  background: #fafafa;
  min-height: 100vh;
}

.page-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.search-input {
  width: 50%;
  padding: 0.7rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border 0.3s;
}

.search-input:focus {
  border-color: #ff9800;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #555;
}

.sweets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.sweet-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.25s, box-shadow 0.25s;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.sweet-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
}

.image-container {
  width: 100%;
  height: 160px;
  overflow: hidden;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.sweet-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.image-container:hover .sweet-image {
  transform: scale(1.1);
}

.sweet-title {
  font-size: 1.2rem;
  color: #ff5722;
  margin-bottom: 0.3rem;
}

.sweet-description {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 0.5rem;
  min-height: 35px;
}

.sweet-price {
  font-size: 1.1rem;
  font-weight: bold;
  color: #2e7d32;
  margin-bottom: 0.3rem;
}

.sweet-qty {
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.in-stock {
  color: #388e3c;
}

.out-of-stock {
  color: #d32f2f;
  font-weight: bold;
}

.purchase-btn {
  width: 100%;
  padding: 0.6rem;
  border: none;
  border-radius: 8px;
  background: #ff9800;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.purchase-btn:hover:not(:disabled) {
  background: #e68900;
}

.purchase-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
