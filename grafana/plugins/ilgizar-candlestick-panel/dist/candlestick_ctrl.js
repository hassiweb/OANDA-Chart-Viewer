'use strict';

System.register(['app/plugins/sdk', 'lodash', 'app/core/utils/kbn', 'app/core/time_series', './rendering', './colors', 'app/core/app_events'], function (_export, _context) {
  "use strict";

  var MetricsPanelCtrl, _, kbn, TimeSeries, rendering, colors, appEvents, _typeof, _createClass, CandleStickCtrl;

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  function _possibleConstructorReturn(self, call) {
    if (!self) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return call && (typeof call === "object" || typeof call === "function") ? call : self;
  }

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
      }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
  }

  return {
    setters: [function (_appPluginsSdk) {
      MetricsPanelCtrl = _appPluginsSdk.MetricsPanelCtrl;
    }, function (_lodash) {
      _ = _lodash.default;
    }, function (_appCoreUtilsKbn) {
      kbn = _appCoreUtilsKbn.default;
    }, function (_appCoreTime_series) {
      TimeSeries = _appCoreTime_series.default;
    }, function (_rendering) {
      rendering = _rendering.default;
    }, function (_colors) {
      colors = _colors.default;
    }, function (_appCoreApp_events) {
      appEvents = _appCoreApp_events.default;
    }],
    execute: function () {
      _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) {
        return typeof obj;
      } : function (obj) {
        return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
      };

      _createClass = function () {
        function defineProperties(target, props) {
          for (var i = 0; i < props.length; i++) {
            var descriptor = props[i];
            descriptor.enumerable = descriptor.enumerable || false;
            descriptor.configurable = true;
            if ("value" in descriptor) descriptor.writable = true;
            Object.defineProperty(target, descriptor.key, descriptor);
          }
        }

        return function (Constructor, protoProps, staticProps) {
          if (protoProps) defineProperties(Constructor.prototype, protoProps);
          if (staticProps) defineProperties(Constructor, staticProps);
          return Constructor;
        };
      }();

      _export('CandleStickCtrl', CandleStickCtrl = function (_MetricsPanelCtrl) {
        _inherits(CandleStickCtrl, _MetricsPanelCtrl);

        function CandleStickCtrl($scope, $injector, $rootScope) {
          _classCallCheck(this, CandleStickCtrl);

          var _this = _possibleConstructorReturn(this, (CandleStickCtrl.__proto__ || Object.getPrototypeOf(CandleStickCtrl)).call(this, $scope, $injector));

          _this.$rootScope = $rootScope;
          _this.hiddenSeries = {};

          var panelDefaults = {
            datasource: null,
            mode: 'color',
            widthMode: 'auto',
            maxDataPoints: 80,
            candlestickWidth: 9,

            bullColor: '#26ff42',
            bearColor: '#ff4a3a',
            dojiColor: '#c8c9ca',
            solidColor: '#000000',
            barColor: '#000000',

            swapYaxes: true,
            labelY1: null,
            labelY2: null,

            colorizeTooltip: true,
            transparentTooltip: false,
            tooltipFormat: 'YYYY-MM-DD HH:mm:ss',

            indicators: []
          };

          _.defaults(_this.panel, panelDefaults);

          _this.events.on('render', _this.onRender.bind(_this));
          _this.events.on('data-received', _this.onDataReceived.bind(_this));
          _this.events.on('data-error', _this.onDataError.bind(_this));
          _this.events.on('data-snapshot-load', _this.onDataReceived.bind(_this));
          _this.events.on('init-edit-mode', _this.onInitEditMode.bind(_this));
          _this.seriesToAlias();
          return _this;
        }

        _createClass(CandleStickCtrl, [{
          key: 'seriesToAlias',
          value: function seriesToAlias() {
            if (_typeof(this.panel.open) !== 'object') {
              return;
            }
            var value = this.panel.open.alias;
            this.panel.open = value;

            value = this.panel.close.alias;
            this.panel.close = value;

            value = this.panel.low.alias;
            this.panel.low = value;

            value = this.panel.high.alias;
            this.panel.high = value;
          }
        }, {
          key: 'onInitEditMode',
          value: function onInitEditMode() {
            this.addEditorTab('Options', 'public/plugins/ilgizar-candlestick-panel/partials/editor.html', 2);
            this.addEditorTab('Indicators', 'public/plugins/ilgizar-candlestick-panel/partials/indicators.html', 3);
          }
        }, {
          key: 'setUnitFormat',
          value: function setUnitFormat(subItem) {
            this.panel.format = subItem.value;
            this.render();
          }
        }, {
          key: 'onDataError',
          value: function onDataError() {
            this.series = [];
            this.render();
          }
        }, {
          key: 'onRender',
          value: function onRender() {
            if (!this.series) {
              return;
            }

            this.data = this.parseSeries(this.series);

            if (this.panel.seriesOverrides) {
              var _iteratorNormalCompletion = true;
              var _didIteratorError = false;
              var _iteratorError = undefined;

              try {
                for (var _iterator = this.series[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                  var series = _step.value;

                  series.applySeriesOverrides(this.panel.seriesOverrides);
                }
              } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
              } finally {
                try {
                  if (!_iteratorNormalCompletion && _iterator.return) {
                    _iterator.return();
                  }
                } finally {
                  if (_didIteratorError) {
                    throw _iteratorError;
                  }
                }
              }
            }
          }
        }, {
          key: 'parseSeries',
          value: function parseSeries(series) {

            if (series === undefined) {
              return series;
            }
            // series must contain aliased datapoints
            // open, high, low, and close, otherwise
            // do not parse any further.
            var keys = ['open', 'high', 'low', 'close'];
            if (series.filter(function (dp) {
              return keys.indexOf(dp.alias) > -1;
            }).length < 4) {
              return [];
            }

            var result = new Array(4);
            var index = 4;
            for (var i = 0; i < series.length; i++) {
              if (series[i] !== undefined) {
                switch (series[i].alias) {
                  case 'open':
                    result[0] = series[i];
                    break;
                  case 'close':
                    result[1] = series[i];
                    break;
                  case 'low':
                    result[2] = series[i];
                    break;
                  case 'high':
                    result[3] = series[i];
                    break;
                  default:
                    result[index++] = series[i];
                    break;
                }
              }
            }

            return result;
          }
        }, {
          key: 'onDataReceived',
          value: function onDataReceived(dataList) {
            var _this2 = this;

            this.series = dataList.map(function (item, index) {
              return _this2.seriesHandler(item, index);
            });
            this.refreshColors();
            this.data = this.parseSeries(this.series);
            this.render(this.data);
          }
        }, {
          key: 'seriesHandler',
          value: function seriesHandler(seriesData, index) {
            var series = new TimeSeries({
              datapoints: seriesData.datapoints,
              alias: seriesData.target
            });

            series.flotpairs = series.getFlotPairs(this.panel.nullPointMode);
            return series;
          }
        }, {
          key: 'refreshColors',
          value: function refreshColors() {
            for (var i = 4; i < this.series.length; i++) {
              if (this.series[i] !== undefined) {
                var index = -1;
                if (this.panel.seriesOverrides !== undefined) {
                  for (var j = 0; j < this.panel.seriesOverrides.length; j++) {
                    if (this.panel.seriesOverrides[j].alias === this.series[i].alias) {
                      index = j;
                      break;
                    }
                  }
                }
                if (index < 0) {
                  if (this.panel.seriesOverrides === undefined) {
                    this.panel.seriesOverrides = [];
                  }
                  index = this.panel.seriesOverrides.length;
                  this.panel.seriesOverrides[index] = {
                    alias: this.series[i].alias,
                    color: colors[index % colors.length],
                    linewidth: 1,
                    fill: 0
                  };
                }
                this.series[i].color = this.panel.seriesOverrides[index].color;
              }
            }
          }
        }, {
          key: 'changeColor',
          value: function changeColor() {
            this.refreshColors();
            this.render();
          }
        }, {
          key: 'link',
          value: function link(scope, elem, attrs, ctrl) {
            rendering(scope, elem, attrs, ctrl);
          }
        }, {
          key: 'toggleSeries',
          value: function toggleSeries(serie) {
            if (this.hiddenSeries[serie.label]) {
              delete this.hiddenSeries[serie.alias];
            } else {
              this.hiddenSeries[serie.label] = true;
            }
            this.render();
          }
        }, {
          key: 'getIndicators',
          value: function getIndicators() {
            return this.series ? _.takeRight(this.series, this.series.length - 4) : [];
          }
        }]);

        return CandleStickCtrl;
      }(MetricsPanelCtrl));

      _export('CandleStickCtrl', CandleStickCtrl);

      CandleStickCtrl.templateUrl = 'partials/module.html';
    }
  };
});
//# sourceMappingURL=candlestick_ctrl.js.map
