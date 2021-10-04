


<script>function dropHandler(ev) {
  console.log('Fichero(s) arrastrados');

  // Evitar el comportamiendo por defecto (Evitar que el fichero se abra/ejecute)
  ev.preventDefault();
  var dict = {}
  if (ev.dataTransfer.items) {
    // Usar la interfaz DataTransferItemList para acceder a el/los archivos)
    for (var i = 0; i < ev.dataTransfer.items.length; i++) {
      // Si los elementos arrastrados no son ficheros, rechazarlos
      if (ev.dataTransfer.items[i].kind === 'file') {
        var file = ev.dataTransfer.items[i].getAsFile();
        dict["file" + i] = file.name
        console.log('... file[' + i + '].name = ' + file.name);
        console.log('valor:' + $("#drop_zone").find("#filename").text());
        $("#drop_zone").find("#filename").text("vamos").trigger('change');
      }
    }
  } else {
    // Usar la interfaz DataTransfer para acceder a el/los archivos
    for (var i = 0; i < ev.dataTransfer.files.length; i++) {
      dict["file" + i] = file.name
      console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
      console.log('valor:' + $("#drop_zone").find("#filename").text());
      $("#filename").text("veeenga").trigger('change');
    }
  }
    console.log("dict" + dict["file0"])
    $.post("/", dict, function(data, status){
    console.log(data + " " + status)})
  // Pasar el evento a removeDragData para limpiar
  removeDragData(ev)
}</script>
    <script>function dragOverHandler(ev) {
  console.log('File(s) in drop zone');

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}</script>
    <script>function removeDragData(ev) {
  console.log('Removing drag data')

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to remove the drag data
    ev.dataTransfer.items.clear();
  } else {
    // Use DataTransfer interface to remove the drag data
    ev.dataTransfer.clearData();
  }
}
</script>

<div id="drop_zone" ondrop="dropHandler(event);" ondragover="dragOverHandler(event);">
        <p>Arrastra y suelta uno o más archivos a esta zona ...</p>
        </div>

