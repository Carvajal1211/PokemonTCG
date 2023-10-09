Vue.component("dropdown", {
  template: `
    <div class="form-group">
      <label class="control-label" v-text="title"></label>
      <input ref="inputRef" class="dataTable-input form-control" v-model="buscador"
             @input="handleInput"
             @focus="focused = true"
             @blur="delayedBlur"
             :placeholder="placeholder" type="text"
      >
      <div class="card table-responsive position-absolute dropdown-menu 
        custom-dropdown-card p-0 m-1 w-100" v-if="focused && (buscador !== '' || showAll)"
        :style="{ width: dropdownWidth + 'px!important' }"
      >
        <table class="table mb-0" id="pc-dt-export">
          <tbody>
            <tr class="table-primary" v-for="item in filteredItems" @click="selectItem(item)">
              <td style="color: #6e6e6e!important; cursor: pointer" v-text="item.name"></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
  props: {
    items: {
      type: Array,
      required: true
    },
    placeholder: {
      type: String,
      default: "Buscar..."
    },
    title: {
      type: String,
      default: ""
    },
    idProperty: {
      type: String,
      required: true
    },
    nombreProperty: {
      type: String,
      required: true
    },
    fetchData: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      dropdownWidth: 0,
      buscador: "",
      selectedItem: null,
      focused: false,
      showAll: true // Añadido para mostrar todos los elementos cuando el input está vacío
    };
  },
  computed: {
    filteredItems() {
      console.log(this.buscador === '' )
      return this.buscador === '' ? this.items : this.items.filter(item =>
        item.name.toLowerCase().includes(this.buscador.toLowerCase())
      );
    }
  },
  methods: {
    //se retrasa un poco el blur para que no se cierre la modal instantaneamente y se pueda emitir la informacion al pad
    delayedBlur() {
      setTimeout(() => {
        this.focused = false;
      }, 100); // Ajusta el tiempo según lo necesario
    },
    handleInput() {
      this.showAll = this.buscador === '' // Actualiza el estado de showAll
    },
    selectItem(item) {
      // console.log(item)
      this.selectedItem = item;
      this.buscador = this.selectedItem.name
      this.$emit('item-selected', this.selectedItem.id); // Emitir evento para el componente padre
    }
  },
  mounted() {
    this.dropdownWidth = this.$refs.inputRef.offsetWidth;
  }
});