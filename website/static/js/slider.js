(() => {
  const visualizer = $($(".visualizer")[0]);
  const items = $(".item-data"),
    title = $(".title"),
    description = $(".description");

  console.log(items, title, description);

  items.hover(function () {
    const $el = $(this);
    visualizer.one("load", () => {
      title.text($el.attr("data-title"));
      description.text($el.attr("data-description"));
    });
    visualizer.attr("src", $el.attr("data-imagem"));
  });
})();
