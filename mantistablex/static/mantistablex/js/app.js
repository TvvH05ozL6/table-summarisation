let handsontable;

function fixAdminLTELayout (callback) {
  // fix adminLTE incompatibility between fixed layout and !expandOnHover sidebar
  // remove fixed from HTML
  // set height to content-wrapper
  // sidebar overflow is disabled -> use only if you have a short nav in sidebar
  if ($('body').hasClass('sde-fixed')) {
    // $("body").removeClass('sde-fixed');

    const headerHeight = $('.main-header').height();
    // console.log($(window).width());
    $('.content-wrapper').css('max-height', `calc(100vh - ${headerHeight}px)`);

    setInterval(function () {
      $('.content-wrapper').css('min-height', `calc(100vh - ${headerHeight}px)`);
    }, 200);

    if ($('.multiStep-horizontal').length !== 0) {

      $('section.content').css('height', `calc(100vh - ${headerHeight}px - 75px)`);
    } else {
      $('section.content').css('height', `calc(100vh - ${headerHeight}px)`);
    }

//        $('body, .wrapper').addClass('overflow-hidden');
  }

  if (typeof callback === 'function') {
    callback();
  }
}

$(function () {
  // fix adminLTE incompatibility between fixed layout and !expandOnHover sidebar
  // remove fixed from HTML
  // set height to content-wrapper
  // sidebar overflow is disabled -> use only if you have a short nav in sidebar
  fixAdminLTELayout();

  // if "multi-step" is in sidebar, add scrollbar
  setTimeout(function () {
    const sideBarMenuHeight = $('.sidebar-menu.tree').height();

    $('.multiStepScrollbar').slimScroll({
      height: `calc(100vh - 100px - ${sideBarMenuHeight}px)`,
      size: '3px',
    });
  }, 500);

  // rerender handsontable when click to open/close sidebar
  $('.sidebar-toggle').click(function () {
    reRenderHandsontable();
  });

  // open/close console
  $('#toggle-console').click(function () {
    $('.sticky-footer').toggleClass('close-console');
    $('.sticky-footer').toggleClass('open-console');
    $('.up-down-arrow').toggleClass('fa-caret-up');
    $('.up-down-arrow').toggleClass('fa-caret-down');
    $('.scrollable-area').slimScroll({
      height: '120px', //scrollable-area height-padding
    });
    reRenderHandsontable();
    calcControlSidebarHeight();
  });

  // open/close horizontal multistep
  $('.multiStep-horizontal .close-multistep').click(function () {
    $('.multiStep-horizontal').toggleClass('closed');
    if ($('.multiStep-horizontal').hasClass('closed'))
      $('section.content').css('height', 'calc(100vh - 50px - 40px)');
    else
      $('section.content').css('height', 'calc(100vh - 50px - 75px)');

    reRenderHandsontable();
    setTimeout(function () {
      calcControlSidebarHeight();
    }, 300);
  });

  $('.multiStep-horizontal .step-box.active').prevAll().addClass('done');

  // close sidebar control
  $('.control-sidebar .close').click(function () {
    closeRightSidebar();
  });

  // change white-space on cell hover
  $('#handsontable tr td').on('mouseenter', function () {
    $(this).css('white-space', 'normal');
  });
  $('#handsontable tr td').on('mouseleave', function () {
    $(this).css('white-space', 'nowrap');
  });

  // add cancel icon when typing in in search bar
  $('.search input').on('keyup', function () {
    const searchVal = $('input#search').val();
    if (searchVal !== '') {
      $('.search .btn-cancel').show();
    } else {
      $('.search .btn-cancel').hide();
    }
  });

  // clear search when click on cancel icon
  $('.search .btn-cancel').click(function () {
    $('.search input').val('');
    $('.search .btn-cancel').hide();
  });

  // filter click
  $('.filter .btn').click(function () {
    if ($(this).hasClass('active')) {
      $('.filter .btn').removeClass('active');
    } else {
      $('.filter .btn').removeClass('active');
      $(this).addClass('active');
    }
  });

  // close sidebar control
  $('.control-sidebar .close').click(function () {
    $('body').removeClass('control-sidebar-open');
    reRenderHandsontable();
  });

  // open/close abstract
  $('.abstract .read-more').click(function () {
    $('.abstract').toggleClass('collapsed');
    if ($('.abstract').hasClass('collapsed')) {
      $('.abstract .read-more').text('Show more');
    } else {
      $('.abstract .read-more').text('Show less');
    }
  });

  // highlight table columns
  $('.highlightCol tbody tr').mouseenter(function () {
    const subColIndex = 1; //TODO dynamic subject column
    updateHandsontableSetting($(this).data('col'), subColIndex);
  });
  $('.highlightCol tbody tr').mouseleave(function () {
    resetHandsontableSettings();
  });

  $('#HOT').click(function () {
    $('body').addClass('control-sidebar-open');
    calcControlSidebarHeight();
    reRenderHandsontable();
  });

  // edit annotations events
  $(document).on('click', '#edit-annotations .edit:not(.disabled):not(.edit-close)', function () {
    const currentRow = $(this).closest('tr');
    const editPanelRow = $(currentRow).next('tr');
    const editPanel = $(editPanelRow).find('.edit-panel');

    // open edit form
    editPanelRow.toggleClass('hiddenRow showRow');
    editPanel.show(300, function () {
      // focus input
      $('input').focus();
    });

    // add class to current row
    currentRow.addClass('edit-mode');

    // change current edit button in close button
    $(this).addClass('edit-close');
    $(this).find('i').toggleClass('fa-window-close fa-pen-square');

    // disable other row edit button
    $('.edit:not(.edit-close)').addClass('disabled');

    // reduce opacity of other row
    $('#relationshipsTable tbody tr').each(function () {
      if (!$(this).is($(currentRow)) && !$(this).hasClass('showRow')) {
        $(this).addClass('opacity-low');
      }
    });

    // set active to subject pencil icon
    $(currentRow).find('.subject .td-icon-edit').addClass('active');

    // adjust prefix space in input
    prefixSpace();

    // highlight column in HOT table
    updateHandsontableSetting($(this).closest('tr').data('col'), 0); //TODO dynamic subject column

  });

  $(document).on('click', '#edit-annotations .edit-close', function () {
    const currentRow = $(this).closest('tr');
    const editPanelRow = $(currentRow).next('tr');
    const editPanel = $(editPanelRow).find('.edit-panel');

    // close edit form
    editPanel.hide(300, function () {
      editPanelRow.toggleClass('hiddenRow showRow');
    });
    currentRow.removeClass('edit-mode');

    // change current close button in edit button
    $(this).removeClass('edit-close');
    $(this).find('i').toggleClass('fa-window-close fa-pen-square');

    // Remove active class to pen icon
    $('.td-icon-edit').removeClass('active');

    // enable row edit button
    $('.edit').removeClass('disabled');

    // remove opacity-low
    $('.relationshipsTable tbody tr').removeClass('opacity-low ');

    // reset HOT settings
    resetHandsontableSettings();
  });

  $('#edit-annotations .td-icon-edit').click(function () {
    // focus input
    $('input').focus();

    const currentTd = $(this).closest('td');

    // Set active class to clicked icon
    $('.td-icon-edit').removeClass('active');
    $(this).addClass('active');

    // adjust prefix space in input
    prefixSpace();

    // reset "save" button
    resetSaveButton();
  });

  $('#edit-annotations .reset-form').click(function () {
    const editPanel = $(this).closest('.edit-panel');

    $(editPanel).find('input').each(function () {
      $(this).val($(this).data('initial-value'));
    });

    $(editPanel).find('select').each(function () {
      const initialValue = $(this).data('initial-value').split(',')[ 0 ];
      $(this).find('option').prop('selected', false);
      $(this).find(`option[value="${initialValue}"]`).prop('selected', true);
    });
  });

  $('#edit-annotations .submit-form').click(function (e) {
    e.stopPropagation();
    e.preventDefault();

    animateSendButton($(this));

    //TODO -> save on DB

  });

  $('#edit-annotations input').on('focus keyup keypress', function (e) {
    // prevent submit form with enter
    var keyCode = e.keyCode || e.which;
    if (keyCode === 13) {
      e.preventDefault();
      return false;
    }
  });

  $('#edit-annotations input').on('keydown', function (e) {
    resetSaveButton();
  });

  $('#edit-annotations select').on('change', function (e) {
    resetSaveButton();
  });

  $('#edit-annotations .use-hint').click(function (e) {
    e.preventDefault();

    const hint = $(this)
      .parent()
      .find('a')
      .text()
      .trim();

    if ($('#edit-annotations input').length > 0) {
      $('#edit-annotations input').val(hint);
    }

    if ($('#edit-annotations select').length > 0) {
      $('#edit-annotations select').val(hint);
    }
    resetSaveButton();
  });

  // ABSTAT autocomplete
  $('#edit-annotations input').on('keyup', function () {
    const input = $(this);

    if (input.data('prev-value') === undefined) {
      input.data('prev-value', input.data('initial-value'));
    }

    let typeCol = 'subj'; //TODO column type (subj, obj, pred)

    if (input.data('prev-value').trim() !== input.val().trim()) {
      getAbstatSuggestion(typeCol, input.val());
    }

    input.data('prev-value', input.val());
  });

  // press up/down key arrow to select one of autocomplete suggestion
  $(document).on('keydown', function (e) {
    const autocompleteDiv = $('#edit-annotations .autocomplete');
    if (autocompleteDiv.hasClass('isVisible')) {
      const firstLi = autocompleteDiv.find('li:first-child');
      const lastLi = autocompleteDiv.find('li:last-child');
      const liActive = autocompleteDiv.find('li.active');
      const liNext = liActive.next();
      const liPrev = liActive.prev();

      switch (e.key) {
        case 'ArrowDown':
          // if an active li does not exist
          if (liActive.length === 0) {
            // add active to first li
            firstLi.addClass('active');
          } else {
            // remove active from li
            liActive.removeClass('active');
            // if active li ha next
            if (liNext.length > 0) {
              // add active to next
              liNext.addClass('active');
            } else {
              // add active to first li
              firstLi.addClass('active');
            }
          }
          break;
        case 'ArrowUp':
          // if an active li does not exist
          if (liActive.length === 0) {
            // add active to last li
            lastLi.addClass('active');
          } else {
            // remove active from li
            liActive.removeClass('active');
            // if active li ha prev
            if (liPrev.length > 0) {
              // add active to prev
              liPrev.addClass('active');
            } else {
              // add active to last li
              lastLi.addClass('active');
            }
          }
          break;
        case 'Enter':
          $('#edit-annotations input').val(liActive.find('.suggestion').text().trim());
          $('#edit-annotations input').blur();
          break;
        default:
          break;
      }
    }
  });

  // click one of autocomplete suggestion
  $(document).on('click', '#edit-annotations .autocomplete li', function (e) {
    e.preventDefault();
    const autocomplete = $(this).find('.suggestion').text().trim();
    $('#edit-annotations  input').val(autocomplete);
    $('#edit-annotations  .autocomplete').removeClass('isVisible');
    resetSaveButton();
  });

  // mouse over autocomplete li
  $(document).on('mouseenter', '#edit-annotations .autocomplete li', function () {
    $('.autocomplete li').removeClass('active');
    $(this).addClass('active');
  });

  // focus/unfocus ul.autocomplete when mouse enter/leave
  $('#edit-annotations .autocomplete').on('mouseenter', function () {
    $(this).addClass('focus');
  });
  $('#edit-annotations .autocomplete').on('mouseleave', function () {
    $(this).removeClass('focus');
  });

  // edit table event
  $('#edit-table-info .submit-form').click(function (e) {
    e.stopPropagation();
    e.preventDefault();

    animateSendButton($(this));

    //TODO -> save on DB

  });

  $('#edit-table-info .reset-form').click(function (e) {
    $('#edit-table-info input').each(function () {
      $(this).val($(this).data('initial-value'));
    });

    if ($('#file').files) {
      $('#file').files[ 0 ] = null;
    }

  });

});

$(window).resize(function () {
  reRenderHandsontable();
});

/* ===============
   HANDSONTABLE
   =============== */

// update HOT to highlight columns
function updateHandsontableSetting (clickedHoveredCol, subColIndex) {

  if (typeof handsontable !== 'undefined') {
    handsontable.updateSettings({
      cells (row, col) {
        if (col !== clickedHoveredCol && col !== subColIndex) {
          handsontable.setCellMeta(this.instance.toVisualRow(row), col, 'className', 'opacity-low');
        }
      },
      afterGetColHeader (col, TH) {
        if (col !== clickedHoveredCol && col !== subColIndex) {
          Handsontable.dom.addClass(TH, 'opacity-low');
        } else {
          Handsontable.dom.removeClass(TH, 'opacity-low');
        }
      },
    });
  }
}

// reset Handsontable Settings
function resetHandsontableSettings () {
  if (typeof handsontable !== 'undefined') {
    handsontable.updateSettings({
      cells (row, col) {
        handsontable.setCellMeta(row, col, 'className', '');
      },
      afterGetColHeader (col, TH) {
        Handsontable.dom.removeClass(TH, 'opacity-low');
      },
    });
  }
}

function reRenderHandsontable () {
  $('.content-wrapper').css('overflow', 'hidden');
  setTimeout(function () {
    const newWidthTable =
      $('body').filter('.inner-control-sidebar.control-sidebar-open').length > 0
        ? $('.content').width() - $('.control-sidebar').width()
        : $('.content').width();

    /*        if (hot1) {
                hot1.updateSettings({
                    height: calcPageContentHeight(),
                    width: newWidthTable,
                });
            }*/
    setTimeout(function () {
      $('.content-wrapper').css('overflow', 'auto');
    }, 2000);
  }, 300);
}

/* ===============
   UTILITIES
   =============== */

//prevent click if btn is disabled
$('.disabled').on('click', function (e) {
  e.preventDefault();
});

/* ===============
   PAGE/SECTION CALC HEIGHT UTILITIES
   =============== */

function calcPageContentHeight () {
  const bodyHeight = '100vh';
  const headerHeight = $('.main-header').height();
  const footerHeight = $('.sticky-footer').outerHeight();
  const multistepHeight = $('.multiStep-horizontal').outerHeight();
  const contentPadding = $('.content').css('padding').replace('px', '') * 2;
  if (!isNaN(multistepHeight))
    return `calc(${bodyHeight} - ${headerHeight}px - ${footerHeight}px - ${contentPadding}px - ${multistepHeight}px)`;

  return `calc(${bodyHeight} - ${headerHeight}px - ${footerHeight}px - ${contentPadding}px)`;
}

function calcControlSidebarHeight () {
  setTimeout(function () {
    let newControlSidebarheigth;
    let newInfoBoxHeight;
    const bodyHeight = '100vh';
    const headerHeight = $('.main-header').height();
    const footerHeight = $('.sticky-footer').outerHeight();
    const multistepHeight = $('.multiStep-horizontal').outerHeight();
    const contentPadding = $('.content').css('padding').replace('px', '') * 2;

    if ($('body').hasClass('inner-control-sidebar')) {
      if (!isNaN(multistepHeight))
        newControlSidebarheigth = newInfoBoxHeight = `calc(${bodyHeight} - ${headerHeight}px - ${footerHeight}px - ${multistepHeight}px)`;
      else
        newControlSidebarheigth = newInfoBoxHeight = `calc(${bodyHeight} - ${headerHeight}px  - ${footerHeight}px`;
    } else {
      newControlSidebarheigth = `calc(${bodyHeight} - ${footerHeight}px`;
      newInfoBoxHeight = `calc(${bodyHeight} - ${headerHeight}px  - ${footerHeight}px`;
    }

    $('.control-sidebar, #infoBox').css('height', newControlSidebarheigth);
    $('#infoBox').slimScroll({
      height: newInfoBoxHeight
    });
  }, 300);

}

// remove schema from url; if url is undefined, return an alternative string
function removeUrlSchema (url, alternativeString) {
  if (url !== undefined && url !== '') {
    if (url.indexOf('XMLSchema#') > -1) {
      return `xsd:${url.toString().split('#').pop()}`;
    }
    return url.toString().split('/').pop();
  }
  return alternativeString;
}

function animateSendButton (button) {
  // animate send button
  $(button).addClass('click');
  $(button).find('span').text('Saved');
}

function chartSetup () {
  const colorsPaletteMonochrome = ['#00a65a', '#128059', '#255A58', '#2F4858', '#4A496E', '#734C90'];
  const dataset = [
    ['no type identified', 5],
    ['id', 80],
    ['hex', 15],
  ];
  dataset.sort(function (a, b) {
    return b[ 1 ] - a[ 1 ];
  });
  dataset.unshift(['LiteralType', 'Percentage']);

  const colors = ['#00a65a', '#128059', '#255A58'];
  const slices = {};

  // Load the Visualization API and the corechart package.
  google.charts.load('current', { packages: ['corechart'] });

  // Set a callback to run when the Google Visualization API is loaded.
  google.charts.setOnLoadCallback(drawChart);

  // Callback that creates and populates a data table,
  // instantiates the pie chart, passes in the data and
  // draws it.
  function drawChart () {
    const data = google.visualization.arrayToDataTable(dataset);

    // Set chart options
    const options = {
      width: '320',
      height: '400',
      chartArea: { width: '320', top: '10', left: '10' },
      pieSliceText: 'label',
      pieSliceTextStyle: { fontSize: '13' },
      legend: { alignment: 'center', position: 'right', textStyle: { fontSize: '13' } },
      tooltip: { showColorCode: true, text: 'percentage' },
      colors,
    };

    // Instantiate and draw our chart, passing in some options.
    const chartContainer = document.getElementById('chart_div');
    if (chartContainer) {
      const chart = new google.visualization.PieChart(chartContainer);
      chart.draw(data, options);
    }
  }

}

// update HOT to highlight columns
function updateHandsontableSetting (clickedHoveredCol, subColIndex) {
  if (typeof hot1 !== 'undefined') {
    hot1.updateSettings({
      cells (row, col) {
        hot1.setCellMeta(row, col, 'className', 'opacity-low');

        if (col !== clickedHoveredCol && col !== subColIndex) {
          hot1.setCellMeta(this.instance.toVisualRow(row), col, 'className', 'opacity-low');
        } else {
          hot1.setCellMeta(row, col, 'className', 'test');
        }
      },
      afterGetColHeader (col, TH) {
        if (col !== clickedHoveredCol && col !== subColIndex) {
          Handsontable.dom.addClass(TH, 'opacity-low');
        } else {
          Handsontable.dom.removeClass(TH, 'opacity-low');
        }
      },
    });
  }
}

// reset Handsontable Settings
function resetHandsontableSettings () {
  if (typeof hot1 !== 'undefined') {
    hot1.updateSettings({
      cells (row, col) {
        hot1.setCellMeta(row, col, 'className', '');
      },
      afterGetColHeader (col, TH) {
        Handsontable.dom.removeClass(TH, 'opacity-low');
      },
    });
  }
}

// adjust prefix space
function prefixSpace () {
  setTimeout(function () {
    const prefixDbo = $('.material.prefix-dbo');
    $(prefixDbo).find('input').css('padding-left', `${$(prefixDbo).find('.prefix').outerWidth() + 3}px`);
  }, 50);
}

// reset "save" button to initial state
function resetSaveButton () {
  const submitBtn = $('.submit-form');
  if (submitBtn.hasClass('click')) {
    submitBtn.removeClass('click');
    submitBtn.find('span').text('Save');
  }
}

// call  from ABSTAT browse api
function callAbstat (queryParam) {
  Session.set('abstatError', undefined);
  const summary = '107dbfc4-0898-40fa-8e48-ab78992b0533';
  const enrichWithSPO = 'false';
  const limit = '10';
  const subtype = 'internal';

  let url = `${'http://backend.abstat.disco.unimib.it/api/v1/browse?'
  + 'enrichWithSPO='}${enrichWithSPO}&limit=${limit}&subtype=${subtype}&summary=${summary}&${queryParam}`;

  url = url.replace(/#/g, '%23');
  // console.log(url);

  $.ajax(url)
    .done(function (results) {
      // TODO abstat return results
    })
    .fail(function () {
      console.log('error');
    });

  // OLD
  // HTTP.call('GET', url, function (error, result) {
  //     if (!error) {
  //         // if literal is Date, join result from Year query
  //         if (queryParam.indexOf('http://www.w3.org/2001/XMLSchema#date') > -1) {
  //             url = url.replace('%23date', '%23gYear');
  //             console.log(url);
  //
  //             HTTP.call('GET', url, function (errorYear, resultYear) {
  //                 if (!error) {
  //                     Session.set('suggestions', $.extend(result.data.akps, resultYear.data.akps));
  //                 } else {
  //                     Session.set('abstatError', true);
  //                 }
  //             });
  //         } else {
  //             Session.set('suggestions', result.data.akps);
  //         }
  //     } else {
  //         console.log(error);
  //         Session.set('suggestions', []);
  //         Session.set('abstatError', true);
  //     }
  // });
}

// call ABSTAT suggestions api
function getAbstatSuggestion (type, input) {
  const limit = '7';
  const dataset = 'dbpedia-2015-10';

  const url = `${'http://backend.abstat.disco.unimib.it/api/v1/SolrSuggestions?'
  + 'qString='}${input}&qPosition=${type}&rows=${limit}&dataset=${dataset}`;

  $.ajax(url)
    .done(function (results) {

      if (results.suggestions) {
        // TODO abstat return autocomplete suggestions
        $('#edit-annotations .autocomplete').empty();
        $('#edit-annotations .autocomplete').addClass('isVisible');

        $(results.suggestions).each(function (index, value) {
          $('#edit-annotations .autocomplete').append(`<li><span class="suggestion"> ${removeUrlSchema(value.suggestion)} </span><span class="text-small">(occurr.: ${value.occurrence})</span></li>`);
        });
      }

    })
    .fail(function () {
      console.log('error');
    });
}

/* ===============
   RIGHT SIDEBAR
   =============== */

// open/close sidebar right
function openRightSidebar () {
  if (!$('#sidebar').length) {
    $('body .control-sidebar').addClass('control-sidebar-open');
    calcControlSidebarHeight();
    //reRenderHandsontable();
  }
}

function closeRightSidebar () {
  $('body .control-sidebar').removeClass('control-sidebar-open');
  calcControlSidebarHeight();
  //reRenderHandsontable();

  /*    if ($.find(".handsontable-col-opacity").length) {
          resetHandsontableSettings();
      }*/

}

function initTable (tableHeader, tableData,
  highlightedData = {},
  tableHeight = `${$('.table-wrapper').height() - $('.bottom-box').height()}`) {


  function formatterValue (value) {

    return '<div class="value">' + value + '</div>';
  }

  function styleCell (value, rowData, rowIndex, colHeader) {
    const colIndex = tableHeader.indexOf(colHeader);
    if (Object.entries(highlightedData).length && (highlightedData.rowIndexes.includes(rowIndex) && highlightedData.colIndexes.includes(colIndex)))
      return { classes: 'highlight' };
    return '';
  }

  var columns = [];

  tableHeader.forEach(element => {
    columns.push({
      field: element,
      title: element,
      // align: 'center',
      valign: 'middle',
      // formatter: formatterValue,
      cellStyle: styleCell
    });
  });
  // console.log(tableData);
  var $table = $('#table-bootstrap');

  $table.bootstrapTable({
    data: tableData,
    columns: columns,
    height: tableHeight
  });

  // $table.on('all.bs.table', function (e, name, args) {
  //   console.log(name, args);
  // });
}

function reInitTable (tableHeader, tableData, highlightedData, tableHeight) {
  $('#table-bootstrap').bootstrapTable('destroy');
  initTable(tableHeader, tableData, highlightedData, tableHeight);
}
