function DelTag(val,asd){
    $("#"+asd).val('');
    $("#"+val).remove();
}

$(document).ready(function(){
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
    $(document).on('change','input',function(){
        ary = $(this).attr('id').split("_");
        item = ary[0];
        z = ary[2];
        DelTag(item+"Preview_"+z+','+item+"_imageInput_"+z);
        let file = this.files[0];
        let PicSrc = URL.createObjectURL(file);
        Pic_str = '<div id="'+item+'Preview_'+z+'" class="Preview_box">';
        Pic_str +='<a class="DelTag" onclick="DelTag('+"'"+item+"Preview_"+z+"'"+','+"'"+item+"_imageInput_"+z+"'"+');">删除</a>';
        Pic_str +='<img src="'+PicSrc+'"/>';
        Pic_str +='</div>';
        $('#'+item+'_append_no_'+z).append(Pic_str);
        
    });
    var list=['relate','summary','exploit']
    list.forEach((item,index)=>{
        $('#'+item+'_add_more').on('click', function(){
            y = parseInt($(this).attr('name'),10);
            x = y + 1;
            var html ='<div id="'+item+'_append_no_'+x+'" class="'+item+'_append_no">'+
                '<textarea class="form-control" rows="3" name="'+item+'_content"></textarea>'+
                '<input id="'+item+'_imageInput_'+x+'" class="form-control imageInput" type="file" accept="image/*" name="'+item+'_image" >'+
                '</div>';
            $(html).insertAfter('#'+item+'_append_no_'+y);
            $(this).attr('name',x);
            
            $('#'+item+'_remove_more').fadeIn(function(){
                $(this).show();
            });
        });
        
        $('#'+item+'_remove_more').on('click', function(){  
            x = parseInt($('#'+item+'_add_more').attr('name'),10);          
            $('#'+item+'_append_no_'+x).remove();
            if (x > 0) {
                x--;
            }
            $('#'+item+'_add_more').attr('name',x);
                        
            if($("."+item+"_append_no").length < 1 ){
                $('#'+item+'_remove_more').fadeOut(function(){
                    $(this).hide()
                });;
            }
        });
        
    })
    
});