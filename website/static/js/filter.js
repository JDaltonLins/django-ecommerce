(() => {
  const tags = $(".tag"),
    categorias = $(".categoria"),
    subcategorias = $(".sub-categoria");

  const filterClickable = (values) => [...values.filter((i, v) => $(v).hasClass("active")).map((i, v) => $(v).attr("data-id"))];

  $(".clickable").on("click", function () {
    const el = $(this);
    el.toggleClass("active");
  });

  $(".filtro > button").click(function () {
    const el = $(this);
    el.addClass("disabled");

    const newUrl = new URLSearchParams();
    const pagina = new URLSearchParams(window.location.search).get("pagina");

    const tagValues = filterClickable(tags).join(","),
      categoriaValues = filterClickable(categorias).join(","),
      subcategoriaValues = filterClickable(subcategorias).join(",");

    if (tagValues.length > 0) {
      newUrl.set("tags", tagValues);
    }
    if (categoriaValues.length > 0) {
      newUrl.set("categorias", categoriaValues);
    }
    if (subcategoriaValues.length > 0) {
      newUrl.set("subcategorias", subcategoriaValues);
    }
    if (pagina) {
      newUrl.set("pagina", pagina);
    }

    window.location.href = `${window.location.pathname}?${newUrl.toString()}`;
  });
})();
