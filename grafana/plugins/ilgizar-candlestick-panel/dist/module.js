'use strict';

System.register(['./candlestick_ctrl', './indicators_ctrl'], function (_export, _context) {
  "use strict";

  var CandleStickCtrl;
  return {
    setters: [function (_candlestick_ctrl) {
      CandleStickCtrl = _candlestick_ctrl.CandleStickCtrl;
    }, function (_indicators_ctrl) {}],
    execute: function () {
      _export('PanelCtrl', CandleStickCtrl);
    }
  };
});
//# sourceMappingURL=module.js.map
