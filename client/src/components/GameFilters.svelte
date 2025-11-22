<script lang="ts">
    import { onMount } from "svelte";

    interface Category {
        id: number;
        name: string;
        description: string;
    }

    interface Publisher {
        id: number;
        name: string;
        description: string;
    }

    export let selectedCategory: number | null = null;
    export let selectedPublisher: number | null = null;

    let categories: Category[] = [];
    let publishers: Publisher[] = [];
    let loadingFilters = true;

    const fetchFilters = async () => {
        try {
            const [categoriesResponse, publishersResponse] = await Promise.all([
                fetch('/api/categories'),
                fetch('/api/publishers')
            ]);

            if (categoriesResponse.ok && publishersResponse.ok) {
                categories = await categoriesResponse.json();
                publishers = await publishersResponse.json();
            }
        } catch (err) {
            console.error('Error fetching filters:', err);
        } finally {
            loadingFilters = false;
        }
    };

    onMount(() => {
        fetchFilters();
    });

    function handleCategoryChange(event: Event) {
        const target = event.target as HTMLSelectElement;
        selectedCategory = target.value ? parseInt(target.value) : null;
    }

    function handlePublisherChange(event: Event) {
        const target = event.target as HTMLSelectElement;
        selectedPublisher = target.value ? parseInt(target.value) : null;
    }

    function clearFilters() {
        selectedCategory = null;
        selectedPublisher = null;
    }
</script>

<div class="mb-8 bg-slate-800/60 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
    <h3 class="text-lg font-semibold text-slate-100 mb-4">Filter Games</h3>
    
    {#if loadingFilters}
        <div class="animate-pulse flex gap-4">
            <div class="h-10 bg-slate-700 rounded w-1/3"></div>
            <div class="h-10 bg-slate-700 rounded w-1/3"></div>
            <div class="h-10 bg-slate-700 rounded w-24"></div>
        </div>
    {:else}
        <div class="flex flex-wrap gap-4">
            <div class="flex-1 min-w-[200px]">
                <label for="category-filter" class="block text-sm font-medium text-slate-300 mb-2">
                    Category
                </label>
                <select
                    id="category-filter"
                    data-testid="category-filter"
                    class="w-full px-4 py-2 bg-slate-900/80 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={selectedCategory || ''}
                    on:change={handleCategoryChange}
                >
                    <option value="">All Categories</option>
                    {#each categories as category}
                        <option value={category.id}>{category.name}</option>
                    {/each}
                </select>
            </div>

            <div class="flex-1 min-w-[200px]">
                <label for="publisher-filter" class="block text-sm font-medium text-slate-300 mb-2">
                    Publisher
                </label>
                <select
                    id="publisher-filter"
                    data-testid="publisher-filter"
                    class="w-full px-4 py-2 bg-slate-900/80 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={selectedPublisher || ''}
                    on:change={handlePublisherChange}
                >
                    <option value="">All Publishers</option>
                    {#each publishers as publisher}
                        <option value={publisher.id}>{publisher.name}</option>
                    {/each}
                </select>
            </div>

            {#if selectedCategory || selectedPublisher}
                <div class="flex items-end">
                    <button
                        data-testid="clear-filters"
                        class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-100 rounded-lg transition-colors duration-200 font-medium"
                        on:click={clearFilters}
                    >
                        Clear Filters
                    </button>
                </div>
            {/if}
        </div>
    {/if}
</div>
