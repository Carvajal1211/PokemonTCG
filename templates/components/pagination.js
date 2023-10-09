
Vue.component("pagination", {
    template:  `
    <div class="container">
        <div class="row">
            <div class="row">
                <div class="col-12 d-flex justify-content-center">
                    <button type="button" class="btn btn btn-outline-primary m-1 btn-sm" @click="$emit('update:page', 1)" style="border-radius: 8px;">Primera</button>
                    <button type="button" class="btn btn-primary m-1" @click="$emit('update:page', currentPage - 1)":disabled="currentPage === 1">Anterior</button>
                    <button v-for="n in (endPage - startPage + 1)" type="button" :class="['btn', 'm-1', n + startPage - 1 === currentPage ? 'btn btn-outline-primary' : 'btn-primary']" style="font-family: monospace;" @click="$emit('update:page', n + startPage - 1)">{{n + startPage - 1}}</button>                    
                    <button type="button" class="btn btn-primary m-1" @click="$emit('update:page', currentPage + 1)":disabled="currentPage === totalPages">Siguiente</button>
                    <button type="button" class="btn btn btn-outline-primary m-1 btn-sm" @click="$emit('update:page', totalPages)" style="border-radius: 8px;">Última</button>
                </div>
            </div>
        </div>
    </div>
    
`,
props: {
    maxVisibleButtons: {
        type: Number,
        required: false,
        default: 3
    },
    totalPages: {
        type: Number,
        required: true
    },
    perPage: {
        type: Number,
        required: true
    },
    currentPage: {
        type: Number,
        required: true
    }
},
computed: {
    startPage() {
        let start = this.currentPage - 2;
        if (start < 1) {
            start = 1;
        }
        if (this.totalPages - start < 4) {
            start = this.totalPages - 4;
        }
        if (start < 1) {
            start = 1;
        }
        return start;
    },
    endPage() {
        let end = this.startPage + 4;
        if (end > this.totalPages) {
            end = this.totalPages;
        }
        return end;
    }
},

methods:{
    goToPage() {
        this.currentPage = this.pageNumber;
    },
    
}
});

