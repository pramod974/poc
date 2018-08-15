import * as service from './service';
import * as embed from './embed';
import * as models from 'powerbi-models';
import * as wpmp from 'window-post-message-proxy';
import * as hpm from 'http-post-message';
import * as utils from './util';
import { Defaults } from './defaults';

/**
 * A Dashboard node within a dashboard hierarchy
 * 
 * @export
 * @interface IDashboardNode
 */
export interface IDashboardNode {
    iframe: HTMLIFrameElement;
    service: service.IService;
    config: embed.IEmbedConfigurationBase
}

/**
 * A Power BI Dashboard embed component
 * 
 * @export
 * @class Dashboard
 * @extends {embed.Embed}
 * @implements {IDashboardNode}
 * @implements {IFilterable}
 */
export class Dashboard extends embed.Embed implements IDashboardNode {
    static allowedEvents = ["tileClicked", "error"];
    static dashboardIdAttribute = 'powerbi-dashboard-id';
    static typeAttribute = 'powerbi-type';
    static type = "Dashboard";

    /**
     * Creates an instance of a Power BI Dashboard.
     * 
     * @param {service.Service} service
     * @param {HTMLElement} element
     */
    constructor(service: service.Service, element: HTMLElement, config: embed.IEmbedConfigurationBase, phasedRender?: boolean) {
        super(service, element, config, /* iframe */ undefined, phasedRender);
        this.loadPath = "/dashboard/load";
        this.phasedLoadPath = "/dashboard/prepare";

        Array.prototype.push.apply(this.allowedEvents, Dashboard.allowedEvents);
    }

    /**
     * This adds backwards compatibility for older config which used the dashboardId query param to specify dashboard id.
     * E.g. https://powerbi-df.analysis-df.windows.net/dashboardEmbedHost?dashboardId=e9363c62-edb6-4eac-92d3-2199c5ca2a9e
     * 
     * By extracting the id we can ensure id is always explicitly provided as part of the load configuration.
     * 
     * @static
     * @param {string} url
     * @returns {string}
     */
    static findIdFromEmbedUrl(url: string): string {
        const dashboardIdRegEx = /dashboardId="?([^&]+)"?/
        const dashboardIdMatch = url.match(dashboardIdRegEx);

        let dashboardId;
        if (dashboardIdMatch) {
            dashboardId = dashboardIdMatch[1];
        }

        return dashboardId;
    }

    /**
     * Get dashboard id from first available location: options, attribute, embed url.
     * 
     * @returns {string}
     */
    getId(): string {
        let config = <embed.IEmbedConfiguration>this.config;
        const dashboardId = config.id || this.element.getAttribute(Dashboard.dashboardIdAttribute) || Dashboard.findIdFromEmbedUrl(config.embedUrl);

        if (typeof dashboardId !== 'string' || dashboardId.length === 0) {
            throw new Error(`Dashboard id is required, but it was not found. You must provide an id either as part of embed configuration or as attribute '${Dashboard.dashboardIdAttribute}'.`);
        }

        return dashboardId;
    }

    /**
     * Validate load configuration.
     */
    validate(baseConfig: embed.IEmbedConfigurationBase): models.IError[] {
      const config = baseConfig as embed.IEmbedConfiguration;
      let error = models.validateDashboardLoad(config);
      return error ? error : this.ValidatePageView(config.pageView);
    }

    /**
     * Populate config for load config
     * 
     * @param {IEmbedConfigurationBase}
     * @returns {void}
     */
    populateConfig(baseConfig: embed.IEmbedConfigurationBase): void {
      let config = <embed.IEmbedConfiguration>baseConfig;

      super.populateConfig(config);

      // TODO: Change when Object.assign is available.
      const settings = utils.assign({}, Defaults.defaultSettings, config.settings);
      config = utils.assign({ settings }, config);

      config.id = this.getId();
      this.config = config;
    }
   
    /**
     * Validate that pageView has a legal value: if page view is defined it must have one of the values defined in models.PageView
     */
    private ValidatePageView(pageView: models.PageView): models.IError[] {
      if (pageView && pageView !== "fitToWidth" && pageView !== "oneColumn" && pageView !== "actualSize") {
        return [{message: "pageView must be one of the followings: fitToWidth, oneColumn, actualSize"}];
      }
    }
}