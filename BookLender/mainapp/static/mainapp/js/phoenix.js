(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('bootstrap')) :
        typeof define === 'function' && define.amd ? define(['bootstrap'], factory) :
        (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.phoenix = factory(global.bootstrap));
})(this, (function (bootstrap) {
    'use strict';

    const docReady = e => {
        "loading" === document.readyState ? document.addEventListener("DOMContentLoaded", e) : setTimeout(e, 1);
    };
    const toggleColor = (e, t) => {
        const o = getItemFromStore("phoenixTheme");
        return "light" === ("auto" === o ? getSystemTheme() : o) ? e : t
    };
    const resize = e => window.addEventListener("resize", e);
    const isIterableArray = e => Array.isArray(e) && !!e.length;
    const camelize = e => {
        const t = e.replace(/[-_\s.]+(.)?/g, ((e, t) => t ? t.toUpperCase() : ""));
        return `${t.substr(0,1).toLowerCase()}${t.substr(1)}`
    };
    const getData = (e, t) => {
        try {
            return JSON.parse(e.dataset[camelize(t)])
        } catch (o) {
            return e.dataset[camelize(t)]
        }
    };
    const hexToRgb = e => {
        let t;
        t = 0 === e.indexOf("#") ? e.substring(1) : e;
        const o = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(t.replace(/^#?([a-f\d])([a-f\d])([a-f\d])$/i, ((e, t, o, r) => t + t + o + o + r + r)));
        return o ? [parseInt(o[1], 16), parseInt(o[2], 16), parseInt(o[3], 16)] : null
    };
    const rgbaColor = (e = "#fff", t = .5) => `rgba(${hexToRgb(e)}, ${t})`;
    const getColor = (e, t = document.documentElement) => getComputedStyle(t).getPropertyValue(`--phoenix-${e}`).trim();
    const hasClass = (e, t) => e.classList.value.includes(t);
    const addClass = (e, t) => {
        e.classList.add(t);
    };
    const getOffset = e => {
        const t = e.getBoundingClientRect(),
            o = window.pageXOffset || document.documentElement.scrollLeft,
            r = window.pageYOffset || document.documentElement.scrollTop;
        return {
            top: t.top + r,
            left: t.left + o
        }
    };
    const isScrolledIntoView = e => {
        let t = e.offsetTop,
            o = e.offsetLeft;
        const r = e.offsetWidth,
            s = e.offsetHeight;
        for (; e.offsetParent;) t += (e = e.offsetParent).offsetTop, o += e.offsetLeft;
        return {
            all: t >= window.pageYOffset && o >= window.pageXOffset && t + s <= window.pageYOffset + window.innerHeight && o + r <= window.pageXOffset + window.innerWidth,
            partial: t < window.pageYOffset + window.innerHeight && o < window.pageXOffset + window.innerWidth && t + s > window.pageYOffset && o + r > window.pageXOffset
        }
    };
    const breakpoints = {
        xs: 0,
        sm: 576,
        md: 768,
        lg: 992,
        xl: 1200,
        xxl: 1540
    };
    const getBreakpoint = e => {
        const t = e && e.classList.value;
        let o;
        return t && (o = breakpoints[t.split(" ").filter((e => e.includes("navbar-expand-"))).pop().split("-").pop()]), o
    };
    const setCookie = (e, t, o) => {
        const r = new Date;
        r.setTime(r.getTime() + o), document.cookie = `${e}=${t};expires=${r.toUTCString()}`;
    };
    const getCookie = e => {
        const t = document.cookie.match(`(^|;) ?${e}=([^;]*)(;|$)`);
        return t ? t[2] : t
    };
    const settings = {
        tinymce: {
            theme: "oxide"
        },
        chart: {
            borderColor: "rgba(255, 255, 255, 0.8)"
        }
    };
    const newChart = (e, t) => {
        const o = e.getContext("2d");
        return new window.Chart(o, t)
    };
    const getItemFromStore = (e, t, o = localStorage) => {
        try {
            return JSON.parse(o.getItem(e)) || t
        } catch {
            return o.getItem(e) || t
        }
    };
    const setItemToStore = (e, t, o = localStorage) => o.setItem(e, t);
    const getStoreSpace = (e = localStorage) => parseFloat((escape(encodeURIComponent(JSON.stringify(e))).length / 1048576).toFixed(2));
    const getDates = (e, t, o = 864e5) => {
        const r = (t - e) / o;
        return Array.from({
            length: r + 1
        }, ((t, r) => new Date(e.valueOf() + o * r)))
    };
    const getPastDates = e => {
        let t;
        switch (e) {
            case "week":
                t = 7;
                break;
            case "month":
                t = 30;
                break;
            case "year":
                t = 365;
                break;
            default:
                t = e;
        }
        const o = new Date,
            r = o,
            s = new Date((new Date).setDate(o.getDate() - (t - 1)));
        return getDates(s, r)
    };
    const getRandomNumber = (e, t) => Math.floor(Math.random() * (t - e) + e);
    const getSystemTheme = () => window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    var utils = {
        docReady: docReady,
        toggleColor: toggleColor,
        resize: resize,
        isIterableArray: isIterableArray,
        camelize: camelize,
        getData: getData,
        hasClass: hasClass,
        addClass: addClass,
        hexToRgb: hexToRgb,
        rgbaColor: rgbaColor,
        getColor: getColor,
        breakpoints: breakpoints,
        getOffset: getOffset,
        isScrolledIntoView: isScrolledIntoView,
        getBreakpoint: getBreakpoint,
        setCookie: setCookie,
        getCookie: getCookie,
        newChart: newChart,
        settings: settings,
        getItemFromStore: getItemFromStore,
        setItemToStore: setItemToStore,
        getStoreSpace: getStoreSpace,
        getDates: getDates,
        getPastDates: getPastDates,
        getRandomNumber: getRandomNumber,
        getSystemTheme: getSystemTheme
    };

    const docComponentInit = () => {
        const e = document.querySelectorAll("[data-component-card]"),
            o = document.getElementById("icon-copied-toast"),
            t = new bootstrap.Toast(o);
        e.forEach((e => {
            const c = e.querySelector(".copy-code-btn"),
                n = e.querySelector(".code-to-copy"),
                d = e.querySelector(".preview-btn"),
                r = e.querySelector(".code-collapse"),
                a = bootstrap.Collapse.getOrCreateInstance(r, {
                    toggle: !1
                });
            d ? .addEventListener("click", (() => {
                a.toggle();
            })), c ? .addEventListener("click", (() => {
                const e = document.createElement("textarea");
                e.value = n.innerHTML, document.body.appendChild(e), e.select(), document.execCommand("copy"), document.body.removeChild(e), o.querySelector(".toast-body").innerHTML = "<code class='text-body-quaternary'>Code has been copied to clipboard.</code>", t.show();
            }));
        }));
    };

    const orders = [{
            id: 1,
            dropdownId: "order-dropdown-1",
            orderId: "#2181",
            mailLink: "mailto:carry@example.com",
            customer: "Carry Anna",
            date: "10/03/2023",
            address: "Carry Anna, 2392 Main Avenue, Penasauka, New Jersey 02149",
            deliveryType: "Cash on Delivery",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$99"
        }, {
            id: 2,
            dropdownId: "order-dropdown-2",
            orderId: "#2182",
            mailLink: "mailto:milind@example.com",
            customer: "Milind Mikuja",
            date: "10/03/2023",
            address: "Milind Mikuja, 1 Hollywood Blvd,Beverly Hills, California 90210",
            deliveryType: "Cash on Delivery",
            status: "Processing",
            badge: {
                type: "primary",
                icon: "fas fa-redo"
            },
            amount: "$120"
        }, {
            id: 3,
            dropdownId: "order-dropdown-3",
            orderId: "#2183",
            mailLink: "mailto:stanly@example.com",
            customer: "Stanly Drinkwater",
            date: "30/04/2023",
            address: "Stanly Drinkwater, 1 Infinite Loop, Cupertino, California 90210",
            deliveryType: "Local Delivery",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$70"
        }, {
            id: 4,
            dropdownId: "order-dropdown-4",
            orderId: "#2184",
            mailLink: "mailto:bucky@example.com",
            customer: "Bucky Robert",
            date: "30/04/2023",
            address: "Bucky Robert, 1 Infinite Loop, Cupertino, California 90210",
            deliveryType: "Free Shipping",
            status: "Pending",
            badge: {
                type: "warning",
                icon: "fas fa-stream"
            },
            amount: "$92"
        }, {
            id: 5,
            dropdownId: "order-dropdown-5",
            orderId: "#2185",
            mailLink: "mailto:josef@example.com",
            customer: "Josef Stravinsky",
            date: "30/04/2023",
            address: "Josef Stravinsky, 1 Infinite Loop, Cupertino, California 90210",
            deliveryType: "Via Free Road",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$120"
        }, {
            id: 6,
            dropdownId: "order-dropdown-6",
            orderId: "#2186",
            mailLink: "mailto:igor@example.com",
            customer: "Igor Borvibson",
            date: "30/04/2023",
            address: "Igor Borvibson, 1 Infinite Loop, Cupertino, California 90210",
            deliveryType: "Free Shipping",
            status: "Processing",
            badge: {
                type: "primary",
                icon: "fas fa-redo"
            },
            amount: "$145"
        }, {
            id: 7,
            dropdownId: "order-dropdown-7",
            orderId: "#2187",
            mailLink: "mailto:katerina@example.com",
            customer: "Katerina Karenin",
            date: "30/04/2023",
            address: "Katerina Karenin, 1 Infinite Loop, Cupertino, California 90210",
            deliveryType: "Flat Rate",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$55"
        }, {
            id: 8,
            dropdownId: "order-dropdown-8",
            orderId: "#2188",
            mailLink: "mailto:roy@example.com",
            customer: "Roy Anderson",
            date: "29/04/2023",
            address: "Roy Anderson, 1 Infinite Loop, Cupertino, California 90210",
            deliveryType: "Local Delivery",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$90"
        }, {
            id: 9,
            dropdownId: "order-dropdown-9",
            orderId: "#2189",
            mailLink: "mailto:Stephenson@example.com",
            customer: "Thomas Stephenson",
            date: "29/04/2023",
            address: "Thomas Stephenson, 116 Ballifeary Road, Bamff",
            deliveryType: "Flat Rate",
            status: "Processing",
            badge: {
                type: "primary",
                icon: "fas fa-redo"
            },
            amount: "$52"
        }, {
            id: 10,
            dropdownId: "order-dropdown-10",
            orderId: "#2190",
            mailLink: "mailto:eviewsing@example.com",
            customer: "Evie Singh",
            date: "29/04/2023",
            address: "Evie Singh, 54 Castledore Road, Tunstead",
            deliveryType: "Flat Rate",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$90"
        }, {
            id: 11,
            dropdownId: "order-dropdown-11",
            orderId: "#2191",
            mailLink: "mailto:peter@example.com",
            customer: "David Peters",
            date: "29/04/2023",
            address: "David Peters, Rhyd Y Groes, Rhosgoch, LL66 0AT",
            deliveryType: "Local Delivery",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$69"
        }, {
            id: 12,
            dropdownId: "order-dropdown-12",
            orderId: "#2192",
            mailLink: "mailto:jennifer@example.com",
            customer: "Jennifer Johnson",
            date: "28/04/2023",
            address: "Jennifer Johnson, Rhyd Y Groes, Rhosgoch, LL66 0AT",
            deliveryType: "Flat Rate",
            status: "Processing",
            badge: {
                type: "primary",
                icon: "fas fa-redo"
            },
            amount: "$112"
        }, {
            id: 13,
            dropdownId: "order-dropdown-13",
            orderId: "#2193",
            mailLink: "mailto:okuneva@example.com",
            customer: "Demarcus Okuneva",
            date: "28/04/2023",
            address: "Demarcus Okuneva, 90555 Upton Drive Jeffreyview, UT 08771",
            deliveryType: "Flat Rate",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$99"
        }, {
            id: 14,
            dropdownId: "order-dropdown-14",
            orderId: "#2194",
            mailLink: "mailto:simeon@example.com",
            customer: "Simeon Harber",
            date: "27/04/2023",
            address: "Simeon Harber, 702 Kunde Plain Apt. 634 East Bridgetview, HI 13134-1862",
            deliveryType: "Free Shipping",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$129"
        }, {
            id: 15,
            dropdownId: "order-dropdown-15",
            orderId: "#2195",
            mailLink: "mailto:lavon@example.com",
            customer: "Lavon Haley",
            date: "27/04/2023",
            address: "Lavon Haley, 30998 Adonis Locks McGlynnside, ID 27241",
            deliveryType: "Free Shipping",
            status: "Pending",
            badge: {
                type: "warning",
                icon: "fas fa-stream"
            },
            amount: "$70"
        }, {
            id: 16,
            dropdownId: "order-dropdown-16",
            orderId: "#2196",
            mailLink: "mailto:ashley@example.com",
            customer: "Ashley Kirlin",
            date: "26/04/2023",
            address: "Ashley Kirlin, 43304 Prosacco Shore South Dejuanfurt, MO 18623-0505",
            deliveryType: "Local Delivery",
            status: "Processing",
            badge: {
                type: "primary",
                icon: "fas fa-redo"
            },
            amount: "$39"
        }, {
            id: 17,
            dropdownId: "order-dropdown-17",
            orderId: "#2197",
            mailLink: "mailto:johnnie@example.com",
            customer: "Johnnie Considine",
            date: "26/04/2023",
            address: "Johnnie Considine, 6008 Hermann Points Suite 294 Hansenville, TN 14210",
            deliveryType: "Flat Rate",
            status: "Pending",
            badge: {
                type: "warning",
                icon: "fas fa-stream"
            },
            amount: "$70"
        }, {
            id: 18,
            dropdownId: "order-dropdown-18",
            orderId: "#2198",
            mailLink: "mailto:trace@example.com",
            customer: "Trace Farrell",
            date: "26/04/2023",
            address: "Trace Farrell, 431 Steuber Mews Apt. 252 Germanland, AK 25882",
            deliveryType: "Free Shipping",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$70"
        }, {
            id: 19,
            dropdownId: "order-dropdown-19",
            orderId: "#2199",
            mailLink: "mailto:nienow@example.com",
            customer: "Estell Nienow",
            date: "26/04/2023",
            address: "Estell Nienow, 4167 Laverna Manor Marysemouth, NV 74590",
            deliveryType: "Free Shipping",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$59"
        }, {
            id: 20,
            dropdownId: "order-dropdown-20",
            orderId: "#2200",
            mailLink: "mailto:howe@example.com",
            customer: "Daisha Howe",
            date: "25/04/2023",
            address: "Daisha Howe, 829 Lavonne Valley Apt. 074 Stehrfort, RI 77914-0379",
            deliveryType: "Free Shipping",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$39"
        }, {
            id: 21,
            dropdownId: "order-dropdown-21",
            orderId: "#2201",
            mailLink: "mailto:haley@example.com",
            customer: "Miles Haley",
            date: "24/04/2023",
            address: "Miles Haley, 53150 Thad Squares Apt. 263 Archibaldfort, MO 00837",
            deliveryType: "Flat Rate",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$55"
        }, {
            id: 22,
            dropdownId: "order-dropdown-22",
            orderId: "#2202",
            mailLink: "mailto:watsica@example.com",
            customer: "Brenda Watsica",
            date: "24/04/2023",
            address: "Brenda Watsica, 9198 O'Kon Harbors Morarborough, IA 75409-7383",
            deliveryType: "Free Shipping",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$89"
        }, {
            id: 23,
            dropdownId: "order-dropdown-23",
            orderId: "#2203",
            mailLink: "mailto:ellie@example.com",
            customer: "Ellie O'Reilly",
            date: "24/04/2023",
            address: "Ellie O'Reilly, 1478 Kaitlin Haven Apt. 061 Lake Muhammadmouth, SC 35848",
            deliveryType: "Free Shipping",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$47"
        }, {
            id: 24,
            dropdownId: "order-dropdown-24",
            orderId: "#2204",
            mailLink: "mailto:garry@example.com",
            customer: "Garry Brainstrow",
            date: "23/04/2023",
            address: "Garry Brainstrow, 13572 Kurt Mews South Merritt, IA 52491",
            deliveryType: "Free Shipping",
            status: "Completed",
            badge: {
                type: "success",
                icon: "fas fa-check"
            },
            amount: "$139"
        }, {
            id: 25,
            dropdownId: "order-dropdown-25",
            orderId: "#2205",
            mailLink: "mailto:estell@example.com",
            customer: "Estell Pollich",
            date: "23/04/2023",
            address: "Estell Pollich, 13572 Kurt Mews South Merritt, IA 52491",
            deliveryType: "Free Shipping",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$49"
        }, {
            id: 26,
            dropdownId: "order-dropdown-26",
            orderId: "#2206",
            mailLink: "mailto:ara@example.com",
            customer: "Ara Mueller",
            date: "23/04/2023",
            address: "Ara Mueller, 91979 Kohler Place Waelchiborough, CT 41291",
            deliveryType: "Flat Rate",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$19"
        }, {
            id: 27,
            dropdownId: "order-dropdown-27",
            orderId: "#2207",
            mailLink: "mailto:blick@example.com",
            customer: "Lucienne Blick",
            date: "23/04/2023",
            address: "Lucienne Blick, 6757 Giuseppe Meadows Geraldinemouth, MO 48819-4970",
            deliveryType: "Flat Rate",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$59"
        }, {
            id: 28,
            dropdownId: "order-dropdown-28",
            orderId: "#2208",
            mailLink: "mailto:haag@example.com",
            customer: "Laverne Haag",
            date: "22/04/2023",
            address: "Laverne Haag, 2327 Kaylee Mill East Citlalli, AZ 89582-3143",
            deliveryType: "Flat Rate",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$49"
        }, {
            id: 29,
            dropdownId: "order-dropdown-29",
            orderId: "#2209",
            mailLink: "mailto:bednar@example.com",
            customer: "Brandon Bednar",
            date: "22/04/2023",
            address: "Brandon Bednar, 25156 Isaac Crossing Apt. 810 Lonborough, CO 83774-5999",
            deliveryType: "Flat Rate",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$39"
        }, {
            id: 30,
            dropdownId: "order-dropdown-30",
            orderId: "#2210",
            mailLink: "mailto:dimitri@example.com",
            customer: "Dimitri Boehm",
            date: "23/04/2023",
            address: "Dimitri Boehm, 71603 Wolff Plains Apt. 885 Johnstonton, MI 01581",
            deliveryType: "Flat Rate",
            status: "On Hold",
            badge: {
                type: "secondary",
                icon: "fas fa-ban"
            },
            amount: "$111"
        }],
        advanceAjaxTableInit = () => {
            const e = (e, a) => {
                    e.disabled = a, e.classList[a ? "add" : "remove"]("disabled");
                },
                a = document.getElementById("advanceAjaxTable");
            if (a) {
                const d = {
                        page: 10,
                        pagination: {
                            item: "<li><button class='page' type='button'></button></li>"
                        },
                        item: e => {
                            const {
                                orderId: a,
                                id: d,
                                customer: o,
                                date: r,
                                address: n,
                                deliveryType: t,
                                status: i,
                                badge: s,
                                amount: l
                            } = e;
                            return `\n          <tr class="btn-reveal-trigger">\n            <td class="order py-2  ps-3 align-middle white-space-nowrap">\n              <a class="fw-semibold" href="https://prium.github.io/phoenix/v1.12.0/apps/e-commerce/admin/order-details.html">\n                ${a}\n              </a>\n            </td>\n            <td class="py-2 align-middle fw-bold">\n              <a class="fw-semibold text-body" href="#!">\n                ${o}\n              </a>\n            </td>\n            <td class="py-2 align-middle">\n              ${r}\n            </td>\n            <td class="py-2 align-middle white-space-nowrap">\n              ${n}\n            </td>\n            <td class="py-2 align-middle white-space-nowrap">\n              <p class="mb-0">${t}</p>\n            </td>\n            <td class="py-2 align-middle text-center fs-8 white-space-nowrap">\n              <span class="badge fs-10 badge-phoenix badge-phoenix-${s.type}">\n                ${i}\n                <span class="ms-1 ${s.icon}" data-fa-transform="shrink-2"></span>\n              </span>\n            </td>\n            <td class="py-2 align-middle text-end fs-8 fw-medium">\n              ${l}\n            </td>\n            <td class="py-2 align-middle white-space-nowrap text-end">\n              <div class="dropstart position-static d-inline-block">\n                <button class="btn btn-link text-body btn-sm dropdown-toggle btn-reveal" type='button' id="order-dropdown-${d}" data-bs-toggle="dropdown" data-boundary="window" aria-haspopup="true" aria-expanded="false" data-bs-reference="parent">\n                  <span class="fas fa-ellipsis-h fs-9"></span>\n                </button>\n                <div class="dropdown-menu dropdown-menu-end border py-2" aria-labelledby="order-dropdown-${d}">\n                  <a href="#!" class="dropdown-item">View</a>\n                  <a href="#!" class="dropdown-item">Edit</a>\n                  <div class"dropdown-divider"></div>\n                  <a href="#!" class="dropdown-item text-warning">Archive</a>\n                </div>\n              </div>\n            </td>\n          </tr>\n        `
                        }
                    },
                    o = a.querySelector('[data-list-pagination="next"]'),
                    r = a.querySelector('[data-list-pagination="prev"]'),
                    n = a.querySelector('[data-list-view="*"]'),
                    t = a.querySelector('[data-list-view="less"]'),
                    i = a.querySelector("[data-list-info]"),
                    s = document.querySelector("[data-list-filter]"),
                    l = new window.List(a, d, orders);
                l.on("updated", (e => {
                    const o = a.querySelector(".fallback") || document.getElementById(d.fallback);
                    o && (0 === e.matchingItems.length ? o.classList.remove("d-none") : o.classList.add("d-none"));
                }));
                const p = l.items.length,
                    c = l.page,
                    m = l.listContainer.querySelector(".btn-close");
                let u = Math.ceil(p / c),
                    y = l.visibleItems.length,
                    f = 1;
                m && m.addEventListener("search.close", (() => l.fuzzySearch("")));
                const w = () => {
                    i && (i.innerHTML = `${l.i} to ${y} of ${p}`), r && e(r, 1 === f), o && e(o, f === u), f > 1 && f < u && (e(o, !1), e(r, !1));
                };
                w(), o && o.addEventListener("click", (e => {
                    e.preventDefault(), f += 1;
                    const a = l.i + c;
                    a <= l.size() && l.show(a, c), y += l.visibleItems.length, w();
                })), r && r.addEventListener("click", (e => {
                    e.preventDefault(), f -= 1, y -= l.visibleItems.length;
                    const a = l.i - c;
                    a > 0 && l.show(a, c), w();
                }));
                const g = () => {
                    t.classList.toggle("d-none"), n.classList.toggle("d-none");
                };
                if (n && n.addEventListener("click", (() => {
                        l.show(1, p), u = 1, f = 1, y = p, w(), g();
                    })), t && t.addEventListener("click", (() => {
                        l.show(1, c), u = Math.ceil(p / c), f = 1, y = l.visibleItems.length, w(), g();
                    })), d.pagination && a.querySelector(".pagination").addEventListener("click", (e => {
                        "page" === e.target.classList[0] && (f = Number(e.target.innerText), w());
                    })), d.filter) {
                    const {
                        key: e
                    } = d.filter;
                    s.addEventListener("change", (a => {
                        l.filter((d => "" === a.target.value || d.values()[e].toLowerCase().includes(a.target.value.toLowerCase())));
                    }));
                }
            }
        };

    const anchorJSInit = () => {
        new window.AnchorJS({
            icon: "#"
        }).add("[data-anchor]");
    };

    const bigPictureInit = () => {
        const {
            getData: e
        } = window.phoenix.utils;
        if (window.BigPicture) {
            document.querySelectorAll("[data-bigpicture]").forEach((i => {
                const t = e(i, "bigpicture"),
                    c = {
                        el: i,
                        noLoader: !0,
                        allowfullscreen: !0
                    },
                    n = window._.merge(c, t);
                i.addEventListener("click", (() => {
                    window.BigPicture(n);
                }));
            }));
        }
    };

    class DomNode {
        constructor(s) {
            this.node = s;
        }
        addClass(s) {
            this.isValidNode() && this.node.classList.add(s);
        }
        removeClass(s) {
            this.isValidNode() && this.node.classList.remove(s);
        }
        toggleClass(s) {
            this.isValidNode() && this.node.classList.toggle(s);
        }
        hasClass(s) {
            this.isValidNode() && this.node.classList.contains(s);
        }
        data(s) {
            if (this.isValidNode()) try {
                return JSON.parse(this.node.dataset[this.camelize(s)])
            } catch (t) {
                return this.node.dataset[this.camelize(s)]
            }
            return null
        }
        attr(s) {
            return this.isValidNode() && this.node[s]
        }
        setAttribute(s, t) {
            this.isValidNode() && this.node.setAttribute(s, t);
        }
        removeAttribute(s) {
            this.isValidNode() && this.node.removeAttribute(s);
        }
        setProp(s, t) {
            this.isValidNode() && (this.node[s] = t);
        }
        on(s, t) {
            this.isValidNode() && this.node.addEventListener(s, t);
        }
        isValidNode() {
            return !!this.node
        }
        camelize(s) {
            const t = s.replace(/[-_\s.]+(.)?/g, ((s, t) => t ? t.toUpperCase() : ""));
            return `${t.substr(0,1).toLowerCase()}${t.substr(1)}`
        }
    }

    const elementMap = new Map;
    class BulkSelect {
        constructor(e, t) {
            this.element = e, this.option = {
                displayNoneClassName: "d-none",
                ...t
            }, elementMap.set(this.element, this);
        }
        static getInstance(e) {
            return elementMap.has(e) ? elementMap.get(e) : null
        }
        init() {
            this.attachNodes(), this.clickBulkCheckbox(), this.clickRowCheckbox();
        }
        getSelectedRows() {
            return Array.from(this.bulkSelectRows).filter((e => e.checked)).map((e => getData(e, "bulk-select-row")))
        }
        attachNodes() {
            const {
                body: e,
                actions: t,
                replacedElement: s
            } = getData(this.element, "bulk-select");
            this.actions = new DomNode(document.getElementById(t)), this.replacedElement = new DomNode(document.getElementById(s)), this.bulkSelectRows = document.getElementById(e).querySelectorAll("[data-bulk-select-row]");
        }
        attachRowNodes(e) {
            this.bulkSelectRows = e;
        }
        clickBulkCheckbox() {
            this.element.addEventListener("click", (() => {
                if ("indeterminate" === this.element.indeterminate) return this.actions.addClass(this.option.displayNoneClassName), this.replacedElement.removeClass(this.option.displayNoneClassName), this.removeBulkCheck(), void this.bulkSelectRows.forEach((e => {
                    const t = new DomNode(e);
                    t.checked = !1, t.setAttribute("checked", !1);
                }));
                this.toggleDisplay(), this.bulkSelectRows.forEach((e => {
                    e.checked = this.element.checked;
                }));
            }));
        }
        clickRowCheckbox() {
            this.bulkSelectRows.forEach((e => {
                new DomNode(e).on("click", (() => {
                    "indeterminate" !== this.element.indeterminate && (this.element.indeterminate = !0, this.element.setAttribute("indeterminate", "indeterminate"), this.element.checked = !0, this.element.setAttribute("checked", !0), this.actions.removeClass(this.option.displayNoneClassName), this.replacedElement.addClass(this.option.displayNoneClassName)), [...this.bulkSelectRows].every((e => e.checked)) && (this.element.indeterminate = !1, this.element.setAttribute("indeterminate", !1)), [...this.bulkSelectRows].every((e => !e.checked)) && (this.removeBulkCheck(), this.toggleDisplay());
                }));
            }));
        }
        removeBulkCheck() {
            this.element.indeterminate = !1, this.element.removeAttribute("indeterminate"), this.element.checked = !1, this.element.setAttribute("checked", !1);
        }
        toggleDisplay() {
            this.actions.toggleClass(this.option.displayNoneClassName), this.replacedElement.toggleClass(this.option.displayNoneClassName);
        }
    }
    const bulkSelectInit = () => {
        const e = document.querySelectorAll("[data-bulk-select");
        e.length && e.forEach((e => {
            new BulkSelect(e).init();
        }));
    };

    const {
        merge: merge$2
    } = window._;
    const echartSetOption = (e, t, o, r) => {
        const {
            breakpoints: a,
            resize: n
        } = window.phoenix.utils, s = t => {
            Object.keys(t).forEach((o => {
                window.innerWidth > a[o] && e.setOption(t[o]);
            }));
        }, i = document.body;
        e.setOption(merge$2(o(), t));
        const c = document.querySelector(".navbar-vertical-toggle");
        c && c.addEventListener("navbar.vertical.toggle", (() => {
            e.resize(), r && s(r);
        })), n((() => {
            e.resize(), r && s(r);
        })), r && s(r), i.addEventListener("clickControl", (({
            detail: {
                control: r
            }
        }) => {
            "phoenixTheme" === r && e.setOption(window._.merge(o(), t));
        }));
    };
    const echartTabs = document.querySelectorAll("[data-tab-has-echarts]");
    echartTabs && echartTabs.forEach((e => {
        e.addEventListener("shown.bs.tab", (e => {
            const t = e.target,
                {
                    hash: o
                } = t,
                r = o || t.dataset.bsTarget,
                a = document.getElementById(r.substring(1)) ? .querySelector("[data-echart-tab]");
            a && window.echarts.init(a).resize();
        }));
    }));

    const basicEchartsInit = () => {
        const {
            getColor: t,
            getData: o,
            getDates: e
        } = window.phoenix.utils;
        document.querySelectorAll("[data-echarts]").forEach((r => {
            const a = o(r, "echarts"),
                i = window.echarts.init(r);
            echartSetOption(i, a, (() => ({
                color: t("primary"),
                tooltip: {
                    trigger: "item",
                    padding: [7, 10],
                    backgroundColor: t("body-highlight-bg"),
                    borderColor: t("border-color"),
                    textStyle: {
                        color: t("light-text-emphasis")
                    },
                    borderWidth: 1,
                    transitionDuration: 0
                },
                xAxis: {
                    type: "category",
                    data: e(new Date("5/1/2022"), new Date("5/7/2022"), 864e5),
                    show: !0,
                    boundaryGap: !1,
                    axisLine: {
                        show: !0,
                        lineStyle: {
                            color: t("secondary-bg")
                        }
                    },
                    axisTick: {
                        show: !1
                    },
                    axisLabel: {
                        formatter: t => window.dayjs(t).format("DD MMM"),
                        interval: 6,
                        showMinLabel: !0,
                        showMaxLabel: !0,
                        color: t("secondary-color")
                    }
                },
                yAxis: {
                    show: !1,
                    type: "value",
                    boundaryGap: !1
                },
                series: [{
                    type: "bar",
                    symbol: "none"
                }],
                grid: {
                    left: 22,
                    right: 22,
                    top: 0,
                    bottom: 20
                }
            })));
        }));
    };

    const reportsDetailsChartInit = () => {
        const {
            getColor: t,
            getData: o,
            toggleColor: e
        } = window.phoenix.utils, i = document.querySelector(".echart-reports-details"), r = (t, o = "MMM DD") => {
            let e = "";
            return t.forEach((t => {
                e += `<div class='ms-1'>\n          <h6 class="text-body-tertiary"><span class="fas fa-circle me-1 fs-10" style="color:${t.color}"></span>\n            ${t.seriesName} : ${"object"==typeof t.value?t.value[1]:t.value}\n          </h6>\n        </div>`;
            })), `<div>\n              <p class='mb-2 text-body-tertiary'>\n                ${window.dayjs(t[0].axisValue).isValid()?window.dayjs(t[0].axisValue).format("DD MMM, YYYY"):t[0].axisValue}\n              </p>\n              ${e}\n            </div>`
        }, a = [64, 40, 45, 62, 82];
        if (i) {
            const l = o(i, "echarts"),
                n = window.echarts.init(i);
            echartSetOption(n, l, (() => ({
                color: [t("primary-lighter"), t("info-light")],
                tooltip: {
                    trigger: "axis",
                    padding: [7, 10],
                    backgroundColor: t("body-highlight-bg"),
                    borderColor: t("border-color"),
                    textStyle: {
                        color: t("light-text-emphasis")
                    },
                    borderWidth: 1,
                    transitionDuration: 0,
                    axisPointer: {
                        type: "none"
                    },
                    formatter: r
                },
                xAxis: {
                    type: "category",
                    data: ["Analysis", "Statement", "Action", "Offering", "Interlocution"],
                    axisLabel: {
                        color: t("body-color"),
                        fontFamily: "Nunito Sans",
                        fontWeight: 600,
                        fontSize: 12.8,
                        rotate: 30,
                        formatter: t => `${t.slice(0,5)}...`
                    },
                    axisLine: {
                        lineStyle: {
                            color: t("secondary-bg")
                        }
                    },
                    axisTick: !1
                },
                yAxis: {
                    type: "value",
                    splitLine: {
                        lineStyle: {
                            color: t("secondary-bg")
                        }
                    },
                    axisLabel: {
                        color: t("body-color"),
                        fontFamily: "Nunito Sans",
                        fontWeight: 700,
                        fontSize: 12.8,
                        margin: 24,
                        formatter: t => `${t}%`
                    }
                },
                series: [{
                    name: "Revenue",
                    type: "bar",
                    barWidth: "32px",
                    barGap: "48%",
                    showBackground: !0,
                    backgroundStyle: {
                        color: e(t("primary-bg-subtle"), t("body-highlight-bg"))
                    },
                    label: {
                        show: !1
                    },
                    itemStyle: {
                        color: e(t("primary-light"), t("primary"))
                    },
                    data: a
                }],
                grid: {
                    right: "0",
                    left: "0",
                    bottom: 0,
                    top: 10,
                    containLabel: !0
                },
                animation: !1
            })));
        }
    };

    const chatInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, t = ".chat-sidebar", a = ".chat-textarea", c = "[data-chat-thread]", r = "[data-chat-thread-tab]", o = "[data-chat-thread-tab-content]", s = document.querySelector(t), l = document.querySelector(a), n = document.querySelectorAll(c), d = document.querySelector(r), i = document.querySelector(o);
        if (d) {
            const t = d.querySelectorAll("[data-bs-toggle='tab']"),
                a = new window.List(i, {
                    valueNames: ["read", "unreadItem"]
                }),
                c = document.querySelector(".chat .card-body");
            c.scrollTop = c.scrollHeight, t.forEach((t => t.addEventListener("shown.bs.tab", (() => {
                const c = e(t, "chat-thread-list");
                a.filter((e => "all" === c || e.elm.classList.contains(c)));
            }))));
        }
        n.forEach((e => {
            e.addEventListener("click", (() => {
                if (s.classList.remove("show"), e.classList.contains("unread")) {
                    e.classList.remove("unread");
                    const t = e.querySelector(".unread-badge");
                    t && t.remove();
                }
            }));
        })), l && l.setAttribute("placeholder", "Type your message...");
    };

    const choicesInit = () => {
        const {
            getData: e
        } = window.phoenix.utils;
        if (window.Choices) {
            document.querySelectorAll("[data-choices]").forEach((t => {
                const i = e(t, "options"),
                    s = new window.Choices(t, {
                        itemSelectText: "",
                        addItems: !0,
                        ...i
                    });
                return document.querySelectorAll(".needs-validation").forEach((e => {
                    const i = () => {
                        e.querySelectorAll(".choices").forEach((e => {
                            const t = e.querySelector(".choices__list--single"),
                                i = e.querySelector(".choices__list--multiple");
                            e.querySelector("[required]") && (t && ("" !== t.querySelector(".choices__item--selectable") ? .getAttribute("data-value") ? (e.classList.remove("invalid"), e.classList.add("valid")) : (e.classList.remove("valid"), e.classList.add("invalid"))), i && (e.getElementsByTagName("option").length ? (e.classList.remove("invalid"), e.classList.add("valid")) : (e.classList.remove("valid"), e.classList.add("invalid"))));
                        }));
                    };
                    e.addEventListener("submit", (() => {
                        i();
                    })), t.addEventListener("change", (() => {
                        i();
                    }));
                })), s
            }));
        }
    };

    const copyLink = () => {
        const {
            getData: t
        } = window.phoenix.utils;
        document.querySelectorAll("[data-copy]").forEach((e => {
            const o = new window.bootstrap.Tooltip(e);
            e.addEventListener("mouseover", (() => o.show())), e.addEventListener("mouseleave", (() => o.hide())), e.addEventListener("click", (() => {
                e.setAttribute("data-bs-original-title", "Copied"), o.show();
                const i = t(e, "copy"),
                    a = document.querySelector(i);
                a.select(), navigator.clipboard.writeText(a.value), e.setAttribute("data-bs-original-title", "click to copy");
            }));
        }));
    };

    const countupInit = () => {
        const {
            getData: o
        } = window.phoenix.utils;
        if (window.countUp) {
            document.querySelectorAll("[data-countup]").forEach((t => {
                const {
                    endValue: n,
                    ...u
                } = o(t, "countup"), e = new window.countUp.CountUp(t, n, {
                    duration: 4,
                    ...u
                });
                e.error ? console.error(e.error) : e.start();
            }));
        }
    };

    const createBoardInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, t = "[data-create-board]", r = "[data-wizard-step]", a = "[data-wizard-form]", o = "[data-kanban-step]", n = "[data-board-prev-btn]", c = "[data-custom-color-radio]", d = "submit", l = "show.bs.tab", s = "click", u = "change", i = document.querySelector(t);
        if (i) {
            const m = i.querySelectorAll(r),
                w = Array.from(m).map((e => window.bootstrap.Tab.getOrCreateInstance(e)));
            document.querySelector(n) ? .addEventListener(s, (() => {
                w[w.length - 2].show();
            })), m.length && m.forEach((t => {
                t.addEventListener(l, (() => {
                    const r = e(t, "wizard-step"),
                        a = document.querySelector(o);
                    a && (a.textContent = r);
                }));
            }));
            const b = i.querySelectorAll(a);
            b.forEach(((e, r) => {
                e.addEventListener(d, (e => {
                    e.preventDefault();
                    const a = new FormData(e.target);
                    Object.fromEntries(a.entries());
                    return r + 1 === b.length && window.location.reload(), null
                }));
            }));
            document.querySelector("#customColorInput") ? .addEventListener(u, (e => {
                const t = e.target.value,
                    r = document.querySelector(c);
                r.setAttribute("checked", "checked"), r.value = t;
            }));
        }
    };

    const detectorInit = () => {
        const {
            addClass: e
        } = window.phoenix.utils, {
            is: o
        } = window, i = document.querySelector("html");
        o.opera() && e(i, "opera"), o.mobile() && e(i, "mobile"), o.firefox() && e(i, "firefox"), o.safari() && e(i, "safari"), o.ios() && e(i, "ios"), o.iphone() && e(i, "iphone"), o.ipad() && e(i, "ipad"), o.ie() && e(i, "ie"), o.edge() && e(i, "edge"), o.chrome() && e(i, "chrome"), o.mac() && e(i, "osx"), o.windows() && e(i, "windows"), navigator.userAgent.match("CriOS") && e(i, "chrome");
    };

    const dropdownOnHover = () => {
        const e = document.querySelector("[data-dropdown-on-hover]");
        e && e.addEventListener("mouseover", (e => {
            if (e.target ? .classList.contains("dropdown-toggle") && !e.target.parentNode.className.includes("dropdown-inside") && window.innerWidth > 992) {
                const o = new window.bootstrap.Dropdown(e.target);
                o._element.classList.add("show"), o._menu.classList.add("show"), o._menu.setAttribute("data-bs-popper", "none"), e.target.parentNode.addEventListener("mouseleave", (() => {
                    window.innerWidth > 992 && o.hide();
                }));
            }
        }));
    };

    const {
        merge: merge$1
    } = window._;
    window.Dropzone && (window.Dropzone.autoDiscover = !1);
    const dropzoneInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, o = "[data-dropzone]", r = ".dz-preview", t = ".dz-preview .dz-preview-cover", i = "dz-file-processing", l = "dz-file-complete", n = "dz-processing", s = "options", a = "addedfile", c = "removedfile", d = "complete", u = document.querySelectorAll(o);
        u.length && u.forEach((o => {
            let u = e(o, s);
            u = u || {};
            const m = u.data ? u.data : {},
                p = merge$1({
                    url: "/assets/php/",
                    addRemoveLinks: !1,
                    previewsContainer: o.querySelector(r),
                    previewTemplate: o.querySelector(r).innerHTML,
                    thumbnailWidth: null,
                    thumbnailHeight: null,
                    maxFilesize: 2,
                    autoProcessQueue: !1,
                    filesizeBase: 1e3,
                    init: function () {
                        const e = this;
                        m.length && m.forEach((o => {
                            const r = {
                                name: o.name,
                                size: o.size
                            };
                            e.options.addedfile.call(e, r), e.options.thumbnail.call(e, r, `${o.url}/${o.name}`);
                        })), e.on(a, (function () {
                            "maxFiles" in u && (1 === u.maxFiles && o.querySelectorAll(t).length > 1 && o.querySelector(t).remove(), 1 === u.maxFiles && this.files.length > 1 && this.removeFile(this.files[0]));
                        }));
                    },
                    error(e, o) {
                        if (e.previewElement) {
                            e.previewElement.classList.add("dz-error"), "string" != typeof o && o.error && (o = o.error);
                            for (let r of e.previewElement.querySelectorAll("[data-dz-errormessage]")) r.textContent = o;
                        }
                    }
                }, u);
            o.querySelector(r).innerHTML = "";
            const w = new window.Dropzone(o, p);
            w.on(a, (() => {
                o.querySelector(t) && o.querySelector(t).classList.remove(l), o.classList.add(i);
            })), w.on(c, (() => {
                o.querySelector(t) && o.querySelector(t).classList.remove(n), o.classList.add(l);
            })), w.on(d, (() => {
                o.querySelector(t) && o.querySelector(t).classList.remove(n), o.classList.add(l);
            }));
        }));
    };

    const featherIconsInit = () => {
        window.feather && window.feather.replace({
            width: "16px",
            height: "16px"
        });
    };

    const flatpickrInit = () => {
        const {
            getData: e
        } = window.phoenix.utils;
        document.querySelectorAll(".datetimepicker").forEach((t => {
            const o = e(t, "options");
            window.flatpickr(t, {
                nextArrow: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">\x3c!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --\x3e<path d="M96 480c-8.188 0-16.38-3.125-22.62-9.375c-12.5-12.5-12.5-32.75 0-45.25L242.8 256L73.38 86.63c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0l192 192c12.5 12.5 12.5 32.75 0 45.25l-192 192C112.4 476.9 104.2 480 96 480z"/></svg>',
                prevArrow: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">\x3c!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --\x3e<path d="M224 480c-8.188 0-16.38-3.125-22.62-9.375l-192-192c-12.5-12.5-12.5-32.75 0-45.25l192-192c12.5-12.5 32.75-12.5 45.25 0s12.5 32.75 0 45.25L77.25 256l169.4 169.4c12.5 12.5 12.5 32.75 0 45.25C240.4 476.9 232.2 480 224 480z"/></svg>',
                locale: {
                    firstDayOfWeek: 0,
                    shorthand: ["S", "M", "T", "W", "T", "F", "S"]
                },
                monthSelectorType: "static",
                onDayCreate: (e, t, o, s) => {
                    5 !== s.dateObj.getDay() && 6 !== s.dateObj.getDay() || (s.className += " weekend-days");
                },
                ...o
            });
        }));
    };

    const formValidationInit = () => {
        document.querySelectorAll(".needs-validation").forEach((t => {
            t.addEventListener("submit", (a => {
                t.checkValidity() || (a.preventDefault(), a.stopPropagation()), t.classList.add("was-validated");
            }), !1);
        }));
    };

    const renderCalendar = (e, t) => {
        const {
            merge: r
        } = window._, a = r({
            initialView: "dayGridMonth",
            editable: !0,
            direction: document.querySelector("html").getAttribute("dir"),
            headerToolbar: {
                left: "prev,next today",
                center: "title",
                right: "dayGridMonth,timeGridWeek,timeGridDay"
            },
            buttonText: {
                month: "Month",
                week: "Week",
                day: "Day"
            }
        }, t), n = new window.FullCalendar.Calendar(e, a);
        return n.render(), document.querySelector(".navbar-vertical-toggle") ? .addEventListener("navbar.vertical.toggle", (() => n.updateSize())), n
    };
    const fullCalendarInit = () => {
        const {
            getData: e
        } = window.phoenix.utils;
        document.querySelectorAll("[data-calendar]").forEach((t => {
            const r = e(t, "calendar");
            renderCalendar(t, r);
        }));
    };

    const glightboxInit = () => {
        window.GLightbox && window.GLightbox({
            selector: "[data-gallery]"
        });
    };

    function initMap() {
        const {
            getData: e
        } = window.phoenix.utils, t = document.body, l = document.querySelectorAll("[data-googlemap]");
        if (l.length && window.google) {
            const i = (e, t) => {
                    const l = document.createElement("button");
                    return l.classList.add(t), l.innerHTML = "zoomIn" === t ? '<span class="fas fa-plus text-body-emphasis"></span>' : '<span class="fas fa-minus text-body-emphasis"></span>', l.addEventListener("click", (() => {
                        const l = e.getZoom();
                        "zoomIn" === t && e.setZoom(l + 1), "zoomOut" === t && e.setZoom(l - 1);
                    })), l
                },
                s = {
                    SnazzyCustomLight: [{
                        featureType: "administrative",
                        elementType: "all",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "administrative",
                        elementType: "labels",
                        stylers: [{
                            visibility: "on"
                        }]
                    }, {
                        featureType: "administrative",
                        elementType: "labels.text.fill",
                        stylers: [{
                            color: "#525b75"
                        }]
                    }, {
                        featureType: "administrative",
                        elementType: "labels.text.stroke",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "administrative",
                        elementType: "labels.icon",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "administrative.country",
                        elementType: "geometry.stroke",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#ffffff"
                        }]
                    }, {
                        featureType: "administrative.province",
                        elementType: "geometry.stroke",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "landscape",
                        elementType: "geometry",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#E3E6ED"
                        }]
                    }, {
                        featureType: "landscape.natural",
                        elementType: "labels",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "poi",
                        elementType: "all",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "road",
                        elementType: "all",
                        stylers: [{
                            color: "#eff2f6"
                        }]
                    }, {
                        featureType: "road",
                        elementType: "labels",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "road.arterial",
                        elementType: "all",
                        stylers: [{
                            visibility: "on"
                        }]
                    }, {
                        featureType: "road.arterial",
                        elementType: "geometry",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#eff2f6"
                        }]
                    }, {
                        featureType: "road.arterial",
                        elementType: "labels.text.fill",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#9fa6bc"
                        }]
                    }, {
                        featureType: "road.arterial",
                        elementType: "labels.text.stroke",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "road.local",
                        elementType: "geometry.fill",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#eff2f6"
                        }]
                    }, {
                        featureType: "road.local",
                        elementType: "labels.text.fill",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#9fa6bc"
                        }]
                    }, {
                        featureType: "road.local",
                        elementType: "labels.text.stroke",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit",
                        elementType: "labels.icon",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit.line",
                        elementType: "geometry",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit.line",
                        elementType: "labels.text",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit.station.airport",
                        elementType: "geometry",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit.station.airport",
                        elementType: "labels",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "water",
                        elementType: "geometry",
                        stylers: [{
                            color: "#F5F7FA"
                        }]
                    }, {
                        featureType: "water",
                        elementType: "labels",
                        stylers: [{
                            visibility: "off"
                        }]
                    }],
                    SnazzyCustomDark: [{
                        featureType: "administrative",
                        elementType: "all",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "administrative",
                        elementType: "labels",
                        stylers: [{
                            visibility: "on"
                        }]
                    }, {
                        featureType: "administrative",
                        elementType: "labels.text.fill",
                        stylers: [{
                            color: "#8a94ad"
                        }]
                    }, {
                        featureType: "administrative",
                        elementType: "labels.text.stroke",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "administrative",
                        elementType: "labels.icon",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "administrative.country",
                        elementType: "geometry.stroke",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#000000"
                        }]
                    }, {
                        featureType: "administrative.province",
                        elementType: "geometry.stroke",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "landscape",
                        elementType: "geometry",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#222834"
                        }]
                    }, {
                        featureType: "landscape.natural",
                        elementType: "labels",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "poi",
                        elementType: "all",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "road",
                        elementType: "all",
                        stylers: [{
                            color: "#141824"
                        }]
                    }, {
                        featureType: "road",
                        elementType: "labels",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "road.arterial",
                        elementType: "all",
                        stylers: [{
                            visibility: "on"
                        }]
                    }, {
                        featureType: "road.arterial",
                        elementType: "geometry",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#141824"
                        }]
                    }, {
                        featureType: "road.arterial",
                        elementType: "labels.text.fill",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#525b75"
                        }]
                    }, {
                        featureType: "road.arterial",
                        elementType: "labels.text.stroke",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "road.local",
                        elementType: "geometry.fill",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#141824"
                        }]
                    }, {
                        featureType: "road.local",
                        elementType: "labels.text.fill",
                        stylers: [{
                            visibility: "on"
                        }, {
                            color: "#67718A"
                        }]
                    }, {
                        featureType: "road.local",
                        elementType: "labels.text.stroke",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit",
                        elementType: "labels.icon",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit.line",
                        elementType: "geometry",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit.line",
                        elementType: "labels.text",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit.station.airport",
                        elementType: "geometry",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit.station.airport",
                        elementType: "labels",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "water",
                        elementType: "geometry",
                        stylers: [{
                            color: "#0f111a"
                        }]
                    }, {
                        featureType: "water",
                        elementType: "labels",
                        stylers: [{
                            visibility: "off"
                        }]
                    }]
                };
            l.forEach((l => {
                const o = e(l, "latlng").split(","),
                    r = l.innerHTML,
                    a = e(l, "zoom"),
                    y = l,
                    n = e(l, "phoenixTheme");
                if ("streetview" === e(l, "phoenixTheme")) {
                    const t = e(l, "pov"),
                        i = {
                            position: {
                                lat: Number(o[0]),
                                lng: Number(o[1])
                            },
                            pov: t,
                            zoom: a,
                            gestureHandling: "none",
                            scrollwheel: !1
                        };
                    return new window.google.maps.StreetViewPanorama(y, i)
                }
                const p = {
                        zoom: a,
                        minZoom: 1.2,
                        clickableIcons: !1,
                        zoomControl: !1,
                        zoomControlOptions: {
                            position: window.google.maps.ControlPosition.LEFT
                        },
                        scrollwheel: e(l, "scrollwheel"),
                        disableDefaultUI: !0,
                        center: new window.google.maps.LatLng(o[0], o[1]),
                        styles: "dark" === window.config.config.phoenixTheme ? s.SnazzyCustomDark : s[n || "SnazzyCustomLight"]
                    },
                    f = new window.google.maps.Map(y, p),
                    m = new window.google.maps.InfoWindow({
                        content: r
                    }),
                    T = document.createElement("div");
                T.classList.add("google-map-control-btn");
                const b = i(f, "zoomIn"),
                    u = i(f, "zoomOut");
                T.appendChild(b), T.appendChild(u), f.controls[window.google.maps.ControlPosition.LEFT].push(T);
                const c = new window.google.maps.Marker({
                    position: new window.google.maps.LatLng(o[0], o[1]),
                    map: f
                });
                c.addListener("click", (() => {
                    m.open(f, c);
                })), t && t.addEventListener("clickControl", (({
                    detail: {
                        control: e,
                        value: t
                    }
                }) => {
                    "phoenixTheme" === e && f.set("styles", "dark" === t ? s.SnazzyCustomDark : s.SnazzyCustomLight);
                }));
            }));
        }
    }

    const iconCopiedInit = () => {
        const e = document.getElementById("icon-list"),
            t = document.getElementById("icon-copied-toast"),
            o = new window.bootstrap.Toast(t);
        e && e.addEventListener("click", (e => {
            const n = e.target;
            "INPUT" === n.tagName && (n.select(), n.setSelectionRange(0, 99999), document.execCommand("copy"), t.querySelector(".toast-body").innerHTML = `<span class="fw-black">Copied:</span>  <code>${n.value}</code>`, o.show());
        }));
    };

    const isotopeInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, t = ".isotope-item", o = "[data-sl-isotope]", i = "[data-filter]", a = "[data-filter-nav]", l = "sl-isotope", r = "active";
        if (window.Isotope) {
            const s = document.querySelectorAll(o);
            s.length && s.forEach((o => {
                window.imagesLoaded(o, (() => {
                    o.querySelectorAll(t).forEach((e => {
                        e.style.visibility = "visible";
                    }));
                    const s = e(o, l),
                        n = {
                            itemSelector: t,
                            layoutMode: "packery"
                        },
                        c = window._.merge(n, s),
                        d = new window.Isotope(o, c);
                    return document.querySelector(a) ? .addEventListener("click", (function (e) {
                        const t = e.target.dataset.filter;
                        d.arrange({
                            filter: t
                        }), document.querySelectorAll(i).forEach((e => {
                            e.classList.remove(r);
                        })), e.target.classList.add(r);
                    })), d
                }));
            }));
        }
    };

    const togglePaginationButtonDisable = (e, t) => {
            e.disabled = t, e.classList[t ? "add" : "remove"]("disabled");
        },
        listInit = () => {
            const {
                getData: e
            } = window.phoenix.utils;
            if (window.List) {
                const t = document.querySelectorAll("[data-list]");
                t.length && t.forEach((t => {
                    const a = t.querySelector("[data-bulk-select]");
                    let n = e(t, "list");
                    n.pagination && (n = {
                        ...n,
                        pagination: {
                            item: "<li><button class='page' type='button'></button></li>",
                            ...n.pagination
                        }
                    });
                    const i = t.querySelector('[data-list-pagination="next"]'),
                        s = t.querySelector('[data-list-pagination="prev"]'),
                        l = t.querySelector('[data-list-view="*"]'),
                        o = t.querySelector('[data-list-view="less"]'),
                        c = t.querySelector("[data-list-info]"),
                        r = t.querySelector("[data-list-filter]"),
                        g = new List(t, n);
                    let d = g.items.length;
                    const h = g.page,
                        u = g.listContainer.querySelector(".btn-close");
                    let m = Math.ceil(g.size() / g.page),
                        p = 1,
                        b = (p - 1) * Number(g.page) + g.visibleItems.length,
                        y = !1;
                    u && u.addEventListener("search.close", (() => {
                        g.fuzzySearch("");
                    }));
                    const v = () => {
                        c && (c.innerHTML = `${g.i} to ${b} <span class='text-body-tertiary'> Items of </span>${d}`), s && togglePaginationButtonDisable(s, 1 === p || 0 === p), i && togglePaginationButtonDisable(i, p === m || 0 === p), p > 1 && p < m && (togglePaginationButtonDisable(i, !1), togglePaginationButtonDisable(s, !1));
                    };
                    v(), i && i.addEventListener("click", (e => {
                        e.preventDefault(), p += 1;
                        const t = g.i + h;
                        t <= g.size() && g.show(t, h);
                    })), s && s.addEventListener("click", (e => {
                        e.preventDefault(), p -= 1;
                        const t = g.i - h;
                        t > 0 && g.show(t, h);
                    }));
                    const f = () => {
                        o.classList.toggle("d-none"), l.classList.toggle("d-none");
                    };
                    if (l && l.addEventListener("click", (() => {
                            g.show(1, d), p = 1, f();
                        })), o && o.addEventListener("click", (() => {
                            g.show(1, h), p = 1, f();
                        })), n.pagination && t.querySelector(".pagination").addEventListener("click", (e => {
                            if ("page" === e.target.classList[0]) {
                                const t = Number(e.target.getAttribute("data-i"));
                                t && (g.show(h * (t - 1) + 1, g.page), p = t);
                            }
                        })), n.filter) {
                        const {
                            key: e
                        } = n.filter;
                        r.addEventListener("change", (t => {
                            g.filter((a => "" === t.target.value || (m = Math.ceil(g.matchingItems.length / g.page), p = 1, v(), a.values()[e].toLowerCase().includes(t.target.value.toLowerCase()))));
                        }));
                    }
                    if (a) {
                        window.phoenix.BulkSelect.getInstance(a).attachRowNodes(g.items.map((e => e.elm.querySelector("[data-bulk-select-row]")))), a.addEventListener("change", (() => {
                            g && (a.checked ? g.items.forEach((e => {
                                e.elm.querySelector("[data-bulk-select-row]").checked = !0;
                            })) : g.items.forEach((e => {
                                e.elm.querySelector("[data-bulk-select-row]").checked = !1;
                            })));
                        }));
                    }
                    g.on("searchStart", (() => {
                        y = !0;
                    })), g.on("searchComplete", (() => {
                        y = !1;
                    })), g.on("updated", (e => {
                        m = g.matchingItems.length ? Math.ceil(g.matchingItems.length / g.page) : Math.ceil(g.size() / g.page), b = (p - 1) * Number(g.page) + g.visibleItems.length, v(), y && (p = 0 === g.matchingItems.length ? 0 : 1, d = g.matchingItems.length, b = (0 === p ? 1 : p - 1) * Number(g.page) + g.visibleItems.length, v(), c && (c.innerHTML = `${0===g.matchingItems.length?0:g.i} to ${0===g.matchingItems.length?0:b} <span class='text-body-tertiary'> Items of </span>${g.matchingItems.length}`));
                        const a = t.querySelector(".fallback") || document.getElementById(n.fallback);
                        a && (0 === e.matchingItems.length ? a.classList.remove("d-none") : a.classList.add("d-none"));
                    }));
                }));
            }
        };

    const lottieInit = () => {
        const {
            getData: o
        } = window.phoenix.utils, t = document.querySelectorAll(".lottie");
        t.length && t.forEach((t => {
            const n = o(t, "options");
            window.bodymovin.loadAnimation({
                container: t,
                path: "../img/animated-icons/warning-light.json",
                renderer: "svg",
                loop: !0,
                autoplay: !0,
                name: "Hello World",
                ...n
            });
        }));
    };

    const modalInit = () => {
        const o = document.querySelectorAll("[data-phoenix-modal]");
        o && o.forEach((o => {
            o.addEventListener("shown.bs.modal", (() => {
                o.querySelectorAll("[autofocus=autofocus]").forEach((o => {
                    o.focus();
                }));
            }));
        }));
    };

    const navbarComboInit = () => {
        const {
            getBreakpoint: e,
            getData: n,
            addClass: r,
            hasClass: t,
            resize: o
        } = window.phoenix.utils, a = ".navbar-vertical", c = '[data-navbar-top="combo"]', i = ".collapse", l = "[data-move-container]", s = ".navbar-nav", d = ".navbar-vertical-divider", v = "flex-column", u = document.querySelector(a), m = document.querySelector(c), b = o => {
            const a = e(u),
                c = e(m);
            if (o < c) {
                const e = m.querySelector(i),
                    t = e.innerHTML;
                if (t) {
                    const o = n(m, "move-target"),
                        i = document.querySelector(o);
                    if (e.innerHTML = "", i.insertAdjacentHTML("afterend", `\n            <div data-move-container class='move-container'>\n              <div class='navbar-vertical-divider'>\n                <hr class='navbar-vertical-hr' />\n              </div>\n              ${t}\n            </div>\n          `), a < c) {
                        const e = document.querySelector(l).querySelector(s);
                        r(e, v);
                    }
                }
            } else {
                const e = document.querySelector(l);
                if (e) {
                    const n = e.querySelector(s);
                    t(n, v) && n.classList.remove(v), e.querySelector(d).remove(), m.querySelector(i).innerHTML = e.innerHTML, e.remove();
                }
            }
        };
        b(window.innerWidth), o((() => b(window.innerWidth)));
    };

    const navbarShadowOnScrollInit = () => {
        const a = document.querySelector("[data-navbar-shadow-on-scroll]");
        a && (window.onscroll = () => {
            window.scrollY > 300 ? a.classList.add("navbar-shadow") : a.classList.remove("navbar-shadow");
        });
    };

    const navbarInit = () => {
        const n = document.querySelector("[data-navbar-soft-on-scroll]");
        if (n) {
            const t = window.innerHeight,
                e = () => {
                    let e = window.pageYOffset / t * 2;
                    e >= 1 && (e = 1), n.style.backgroundColor = `rgba(255, 255, 255, ${e})`;
                };
            e(), document.addEventListener("scroll", (() => e()));
        }
    };

    const handleNavbarVerticalCollapsed = () => {
        const {
            getItemFromStore: e,
            setItemToStore: t,
            resize: a
        } = window.phoenix.utils, o = "body", n = ".navbar-vertical", l = ".navbar-vertical-toggle", r = ".navbar-vertical .navbar-collapse", c = ".navbar-vertical .nav-link.active", s = "click", i = "navbar.vertical.toggle", d = "navbar-vertical-collapsed", v = document.querySelector(l), m = document.querySelector(r), u = document.querySelector(c);
        if (v && v.addEventListener(s, (a => {
                const o = e("phoenixIsNavbarVerticalCollapsed", !1);
                v.blur(), document.documentElement.classList.toggle(d), t("phoenixIsNavbarVerticalCollapsed", !o);
                const n = new CustomEvent(i);
                a.currentTarget ? .dispatchEvent(n);
            })), m) {
            const t = e("phoenixIsNavbarVerticalCollapsed", !1);
            u && !t && u.scrollIntoView({
                behavior: "smooth"
            });
        }
        const b = () => {
            const e = document.querySelector(o).offsetHeight,
                t = document.querySelector(n) ? .offsetHeight;
            document.documentElement.classList.contains(d) && e < t ? document.documentElement.style.minHeight = `${t}px` : document.documentElement.removeAttribute("style");
        };
        b(), a((() => {
            b();
        })), v && v.addEventListener("navbar.vertical.toggle", (() => {
            b();
        }));
    };

    const phoenixOffcanvasInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, o = document.querySelectorAll("[data-phoenix-toggle='offcanvas']"), t = document.querySelector("[data-phoenix-backdrop]"), a = document.querySelector("[data-phoenix-scroll]"), c = document.querySelector(".faq"), n = document.querySelector(".faq-sidebar"), s = e => {
            e.classList.remove("show"), document.body.style.removeProperty("overflow");
        };
        o && o.forEach((o => {
            const c = e(o, "phoenix-target"),
                n = document.querySelector(c),
                d = n.querySelectorAll("[data-phoenix-dismiss='offcanvas']");
            o.addEventListener("click", (() => {
                n.classList.add("show"), a || (document.body.style.overflow = "hidden");
            })), d && d.forEach((e => {
                e.addEventListener("click", (() => {
                    s(n);
                }));
            })), t && t.addEventListener("click", (() => {
                s(n);
            }));
        })), c && n.classList.contains("show") && (c.classList.add = "newFaq");
    };

    const picmoInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, t = document.querySelectorAll("[data-picmo]");
        t && Array.from(t).forEach((t => {
            const o = e(t, "picmo"),
                n = window.picmoPopup.createPopup({}, {
                    referenceElement: t,
                    triggerElement: t,
                    position: "bottom-start",
                    showCloseButton: !1
                });
            t.addEventListener("click", (() => {
                n.toggle();
            }));
            const i = document.querySelector(o.inputTarget);
            n.addEventListener("emoji:select", (e => {
                i && (i.innerHTML += e.emoji);
            }));
        }));
    };

    const popoverInit = () => {
        Array.from(document.querySelectorAll('[data-bs-toggle="popover"]')).map((o => new bootstrap.Popover(o)));
    };

    const getThubmnailDirection = () => window.innerWidth < 768 || window.innerWidth >= 992 && window.innerWidth < 1200 ? "horizontal" : "vertical",
        productDetailsInit = () => {
            const {
                getData: e,
                resize: t
            } = window.phoenix.utils, i = document.querySelector("[data-product-details]");
            if (i) {
                const r = i.querySelector("[data-product-color]"),
                    n = (i.querySelector("[data-product-quantity]"), i.querySelector('[data-quantity] input[type="number"]')),
                    a = i.querySelector("[data-product-color-variants]"),
                    c = r => {
                        const n = i.querySelector("[data-products-swiper]"),
                            a = e(n, "swiper"),
                            c = e(n, "thumb-target"),
                            s = document.getElementById(c);
                        let o = "";
                        r.forEach((e => {
                            o += `\n          <div class='swiper-slide '>\n            <img class='w-100' src=${e} alt="">\n          </div>\n        `;
                        })), n.innerHTML = `<div class='swiper-wrapper'>${o}</div>`;
                        let d = "";
                        r.forEach((e => {
                            d += `\n          <div class='swiper-slide '>\n            <div class="product-thumb-container p-2 p-sm-3 p-xl-2">\n              <img src=${e} alt="">\n            </div>\n          </div>\n        `;
                        })), s.innerHTML = `<div class='swiper-wrapper'>${d}</div>`;
                        const l = new window.Swiper(s, {
                                slidesPerView: 5,
                                spaceBetween: 16,
                                direction: getThubmnailDirection(),
                                breakpoints: {
                                    768: {
                                        spaceBetween: 100
                                    },
                                    992: {
                                        spaceBetween: 16
                                    }
                                }
                            }),
                            p = n.querySelector(".swiper-nav");
                        t((() => {
                            l.changeDirection(getThubmnailDirection());
                        })), new Swiper(n, {
                            ...a,
                            navigation: {
                                nextEl: p ? .querySelector(".swiper-button-next"),
                                prevEl: p ? .querySelector(".swiper-button-prev")
                            },
                            thumbs: {
                                swiper: l
                            }
                        });
                    },
                    s = a.querySelectorAll("[data-variant]");
                s.forEach((t => {
                    t.classList.contains("active") && (c(e(t, "products-images")), r.innerHTML = e(t, "variant"));
                    const i = e(t, "products-images");
                    t.addEventListener("click", (() => {
                        c(i), s.forEach((e => {
                            e.classList.remove("active");
                        })), t.classList.add("active"), r.innerHTML = e(t, "variant");
                    }));
                })), n.addEventListener("change", (e => {
                    "" == e.target.value && (e.target.value = 0);
                }));
            }
        };

    const quantityInit = () => {
        const {
            getData: t
        } = window.phoenix.utils, e = "[data-quantity] [data-type]", a = "[data-quantity]", n = '[data-quantity] input[type="number"]', u = "click", i = "min", r = "type";
        document.querySelectorAll(e).forEach((e => {
            e.addEventListener(u, (e => {
                const u = e.currentTarget,
                    l = t(u, r),
                    c = u.closest(a).querySelector(n),
                    o = c.getAttribute(i);
                let y = parseInt(c.value, 10);
                "plus" === l ? y += 1 : y = y > o ? y -= 1 : y, c.value = y;
            }));
        }));
    };

    const randomColorInit = () => {
        const {
            getData: o
        } = window.phoenix.utils, t = document.querySelectorAll("[data-random-color]"), r = ["#85A9FF", "#60C6FF", "#90D67F", "#F48270", "#3874FF", "#0097EB", "#25B003", "#EC1F00", "#E5780B", "#004DFF", "#0080C7", "#23890B", "#CC1B00", "#D6700A", "#222834", "#3E465B", "#6E7891", "#9FA6BC"];
        t.forEach((t => {
            const e = o(t, "random-color");
            let n;
            n = Array.isArray(e) ? [...r, ...e] : [...r], t.addEventListener("click", (o => {
                const t = n[Math.floor(Math.random() * (n.length - 1))];
                o.target.value = t;
                const r = o.target.nextElementSibling;
                r.style.background = `${t}`, r.style.borderColor = `${t}`, r.style.color = "white";
            }));
        }));
    };

    const ratingInit = () => {
        const {
            getData: t,
            getItemFromStore: e
        } = window.phoenix.utils;
        document.querySelectorAll("[data-rater]").forEach((r => {
            const a = {
                reverse: e("phoenixIsRTL"),
                starSize: 32,
                step: .5,
                element: r,
                rateCallback(t, e) {
                    this.setRating(t), e();
                },
                ...t(r, "rater")
            };
            return window.raterJs(a)
        }));
    };

    const responsiveNavItemsInit = () => {
        const {
            resize: e
        } = window.phoenix.utils, t = "[data-nav-item]", l = "[data-navbar]", o = "[data-more-item]", i = "[data-category-list]", n = "[data-category-btn]", s = document.querySelector(l), a = () => {
            const e = s.clientWidth,
                l = s.querySelector(o),
                i = l.clientWidth,
                a = e - i,
                r = s.querySelectorAll(t),
                c = s.querySelector(n).clientWidth;
            let d = 0;
            l.style.display = "none", r.forEach((e => {
                const t = e.clientWidth;
                if (d += t, d + c + i > a && !e.classList.contains("dropdown")) {
                    l.style.display = "block", e.style.display = "none";
                    const t = e.firstChild.cloneNode(!0);
                    s.querySelector(".category-list").appendChild(t);
                }
            }));
            s.querySelectorAll(".dropdown-menu .nav-link").forEach((e => {
                e.classList.remove("nav-link"), e.classList.add("dropdown-item");
            }));
        };
        if (s) {
            window.addEventListener("load", (() => {
                a();
            })), e((() => {
                const e = s.querySelectorAll(t),
                    l = s.querySelectorAll(i);
                e.forEach((e => e.removeAttribute("style"))), l.forEach((e => e.innerHTML = "")), a();
            }));
            const l = s.querySelectorAll(".nav-link");
            s.addEventListener("click", (function (e) {
                for (let e = 0; e < l.length; e++) l[e].classList.remove("active");
                e.target.closest("li") && e.target.closest("li").classList.add("active");
            }));
        }
    };

    const searchInit = () => {
        const e = '[data-bs-dismiss="search"]',
            t = '[data-bs-toggle="dropdown"]',
            s = ".dropdown-menu",
            r = ".search-box",
            c = ".search-input",
            o = '[data-bs-toggle="search"]',
            a = "show",
            n = "aria-expanded",
            d = "click",
            l = "focus",
            u = "show.bs.dropdown",
            i = "search.close",
            h = e => {
                const t = e.querySelector(o),
                    r = e.querySelector(s);
                t && r && (t.setAttribute(n, "false"), t.classList.remove(a), r.classList.remove(a));
            },
            v = document.querySelectorAll(r),
            E = () => {
                v.forEach(h);
            };
        v.forEach((t => {
            const r = t.querySelector(c),
                u = t.querySelector(e),
                v = t.querySelector(s);
            r && r.addEventListener(l, (() => {
                E();
                const e = t.querySelector(o);
                e && v && (e.setAttribute(n, "true"), e.classList.add(a), v.classList.add(a));
            })), document.addEventListener(d, (({
                target: e
            }) => {
                !t.contains(e) && h(t);
            })), u && u.addEventListener(d, (e => {
                h(t), r.value = "";
                const s = new CustomEvent(i);
                e.currentTarget.dispatchEvent(s);
            }));
        })), document.querySelectorAll(t).forEach((e => {
            e.addEventListener(u, (() => {
                E();
            }));
        }));
    };

    const simplebarInit = () => {
        Array.from(document.querySelectorAll(".scrollbar-overlay")).forEach((r => new window.SimpleBar(r)));
    };

    const sortableInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, o = document.querySelectorAll("[data-sortable]"), t = {
            animation: 150,
            group: {
                name: "shared"
            },
            delay: 100,
            delayOnTouchOnly: !0,
            forceFallback: !0,
            onStart() {
                document.body.classList.add("sortable-dragging");
            },
            onEnd() {
                document.body.classList.remove("sortable-dragging");
            }
        };
        o.forEach((o => {
            const a = e(o, "sortable"),
                n = window._.merge(t, a);
            return window.Sortable.create(o, n)
        }));
    };

    const supportChatInit = () => {
        const t = document.querySelector(".support-chat"),
            o = document.querySelectorAll(".btn-support-chat"),
            c = document.querySelector(".support-chat-container"),
            {
                phoenixSupportChat: s
            } = window.config.config;
        s && c ? .classList.add("show"), o && o.forEach((s => {
            s.addEventListener("click", (() => {
                t.classList.toggle("show-chat"), o[o.length - 1].classList.toggle("btn-chat-close"), c.classList.add("show");
            }));
        }));
    };

    const swiperInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, t = document.querySelectorAll(".swiper-theme-container");
        t && t.forEach((t => {
            const r = t.querySelector("[data-swiper]"),
                i = e(r, "swiper"),
                n = i.thumb;
            let s;
            if (n) {
                const e = r.querySelectorAll("img");
                let t = "";
                e.forEach((e => {
                    t += `\n          <div class='swiper-slide '>\n            <img class='img-fluid rounded mt-1' src=${e.src} alt=''/>\n          </div>\n        `;
                }));
                const i = document.createElement("div");
                if (i.setAttribute("class", "swiper thumb"), i.innerHTML = `<div class='swiper-wrapper'>${t}</div>`, n.parent) {
                    document.querySelector(n.parent).parentNode.appendChild(i);
                } else r.parentNode.appendChild(i);
                s = new window.Swiper(i, n);
            }
            const o = t.querySelector(".swiper-nav");
            new window.Swiper(r, {
                ...i,
                navigation: {
                    nextEl: o ? .querySelector(".swiper-button-next"),
                    prevEl: o ? .querySelector(".swiper-button-prev")
                },
                thumbs: {
                    swiper: s
                }
            });
        }));
    };

    const {
        config: config
    } = window.config, initialDomSetup = e => {
        const {
            getData: t,
            getItemFromStore: a,
            getSystemTheme: o
        } = window.phoenix.utils;
        e && e.querySelectorAll("[data-theme-control]").forEach((e => {
            const n = t(e, "theme-control"),
                r = a(n);
            "phoenixNavbarTopShape" === n && "dual-nav" === a("phoenixNavbarPosition") && e.setAttribute("disabled", !0);
            const i = a("phoenixNavbarPosition");
            if ("phoenixNavbarVerticalStyle" === n && ("horizontal" === i || "dual-nav" === i) && e.setAttribute("disabled", !0), "checkbox" === e.type) "phoenixTheme" === n ? ("auto" === r ? "dark" === o() : "dark" === r) && e.setAttribute("checked", !0) : r && e.setAttribute("checked", !0);
            else if ("radio" === e.type && "phoenixNavbarVerticalStyle" === n) "darker" === r && "darker" === e.value && e.setAttribute("checked", !0), "default" === r && "default" === e.value && e.setAttribute("checked", !0);
            else if ("radio" === e.type && "phoenixNavbarTopShape" === n) "slim" === r && "slim" === e.value && e.setAttribute("checked", !0), "default" === r && "default" === e.value && e.setAttribute("checked", !0);
            else if ("radio" === e.type && "phoenixNavbarTopStyle" === n) "darker" === r && "darker" === e.value && e.setAttribute("checked", !0), "default" === r && "default" === e.value && e.setAttribute("checked", !0);
            else if ("radio" === e.type && "phoenixTheme" === n) {
                r === e.value && e.setAttribute("checked", !0);
            } else if ("radio" === e.type && "phoenixNavbarPosition" === n) {
                r === e.value && e.setAttribute("checked", !0);
            } else {
                r === e.value && e.classList.add("active");
            }
        }));
    }, changeTheme = e => {
        const {
            getData: t,
            getItemFromStore: a,
            getSystemTheme: o
        } = window.phoenix.utils;
        e.querySelectorAll('[data-theme-control = "phoenixTheme"]').forEach((e => {
            const n = t(e, "theme-control"),
                r = a(n);
            "checkbox" === e.type ? "auto" === r ? "dark" === o() ? e.checked = !0 : e.checked = !1 : e.checked = "dark" === r : "radio" === e.type ? r === e.value ? e.checked = !0 : e.checked = !1 : r === e.value ? e.classList.add("active") : e.classList.remove("active");
        }));
    }, handleThemeDropdownIcon = e => {
        document.querySelectorAll("[data-theme-dropdown-toggle-icon]").forEach((t => {
            t.classList.toggle("d-none", e !== t.getAttribute("data-theme-dropdown-toggle-icon"));
        }));
    };
    handleThemeDropdownIcon(localStorage.getItem("phoenixTheme"));
    const themeControl = () => {
        const {
            getData: e,
            getItemFromStore: t,
            getSystemTheme: a
        } = window.phoenix.utils, o = t => {
            const a = e(t, "page-url");
            a ? window.location.replace(a) : window.location.reload();
        }, n = new DomNode(document.body), r = document.querySelector(".navbar-vertical"), i = document.querySelector(".navbar-top"), c = document.querySelector(".support-chat-container");
        initialDomSetup(n.node), n.on("click", (e => {
            const d = new DomNode(e.target);
            if (d.data("theme-control")) {
                const l = d.data("theme-control");
                let h = e.target["checkbox" === e.target.type ? "checked" : "value"];
                switch ("phoenixTheme" === l && "boolean" == typeof h && (h = h ? "dark" : "light"), config.hasOwnProperty(l) && window.config.set({
                    [l]: h
                }), window.history.replaceState(null, null, window.location.pathname), l) {
                    case "phoenixTheme": {
                        document.documentElement.setAttribute("data-bs-theme", "auto" === h ? a() : h);
                        const t = new CustomEvent("clickControl", {
                            detail: {
                                control: l,
                                value: h
                            }
                        });
                        e.currentTarget.dispatchEvent(t), changeTheme(n.node);
                        break
                    }
                    case "phoenixNavbarVerticalStyle":
                        r.setAttribute("data-navbar-appearance", "default"), "default" !== h && r.setAttribute("data-navbar-appearance", "darker");
                        break;
                    case "phoenixNavbarTopStyle":
                        i.setAttribute("data-navbar-appearance", "default"), "default" !== h && i.setAttribute("data-navbar-appearance", "darker");
                        break;
                    case "phoenixNavbarTopShape":
                        "dual-nav" === t("phoenixNavbarPosition") ? el.setAttribute("disabled", !0) : o(d.node);
                        break;
                    case "phoenixNavbarPosition":
                        o(d.node);
                        break;
                    case "phoenixIsRTL":
                        window.config.set({
                            phoenixIsRTL: d.node.checked
                        }), window.location.reload();
                        break;
                    case "phoenixSupportChat":
                        c ? .classList.remove("show"), h && c ? .classList.add("show");
                        break;
                    case "reset":
                        window.config.reset(), window.location.reload();
                        break;
                    default:
                        window.location.reload();
                }
            }
        })), n.on("clickControl", (({
            detail: {
                control: e,
                value: t
            }
        }) => {
            "phoenixTheme" === e && handleThemeDropdownIcon(t);
        }));
    };

    const {
        merge: merge
    } = window._, tinymceInit = () => {
        const {
            getColor: e,
            getData: t,
            getItemFromStore: n
        } = window.phoenix.utils, o = document.querySelectorAll("[data-tinymce]");
        if (window.tinymce) {
            o.forEach((o => {
                const i = t(o, "tinymce"),
                    r = merge({
                        selector: ".tinymce",
                        height: "50vh",
                        skin: "oxide",
                        menubar: !1,
                        content_style: `\n        .mce-content-body { \n          color: ${e("emphasis-color")};\n          background-color: ${e("tinymce-bg")};\n        }\n        .mce-content-body[data-mce-placeholder]:not(.mce-visualblocks)::before {\n          color: ${e("quaternary-color")};\n          font-weight: 400;\n          font-size: 12.8px;\n        }\n        `,
                        statusbar: !1,
                        plugins: "link,image,lists,table,media",
                        theme_advanced_toolbar_align: "center",
                        directionality: n("phoenixIsRTL") ? "rtl" : "ltr",
                        toolbar: [{
                            name: "history",
                            items: ["undo", "redo"]
                        }, {
                            name: "formatting",
                            items: ["bold", "italic", "underline", "strikethrough"]
                        }, {
                            name: "alignment",
                            items: ["alignleft", "aligncenter", "alignright", "alignjustify"]
                        }, {
                            name: "list",
                            items: ["numlist", "bullist"]
                        }, {
                            name: "link",
                            items: ["link"]
                        }],
                        setup: e => {
                            e.on("focus", (() => {
                                document.querySelector(".tox-sidebar-wrap").classList.add("editor-focused");
                            })), e.on("blur", (() => {
                                document.querySelector(".tox-sidebar-wrap").classList.remove("editor-focused");
                            }));
                        }
                    }, i);
                window.tinymce.init(r);
            }));
            const i = document.body;
            i && i.addEventListener("clickControl", (({
                detail: {
                    control: t
                }
            }) => {
                "phoenixTheme" === t && o.forEach((t => {
                    window.tinymce.get(t.id).dom.addStyle(`.mce-content-body{\n                  color: ${e("emphasis-color")} !important;\n                  background-color: ${e("tinymce-bg")} !important;\n                }`);
                }));
            }));
        }
    };

    const toastInit = () => {
        [].slice.call(document.querySelectorAll(".toast")).map((t => new bootstrap.Toast(t)));
        const t = document.getElementById("liveToastBtn");
        if (t) {
            const e = new bootstrap.Toast(document.getElementById("liveToast"));
            t.addEventListener("click", (() => {
                e && e.show();
            }));
        }
    };

    const todoOffcanvasInit = () => {
        const {
            getData: o
        } = window.phoenix.utils, t = document.querySelectorAll("[data-event-propagation-prevent]");
        t && t.forEach((o => {
            o.addEventListener("click", (o => {
                o.stopPropagation();
            }));
        }));
        const e = document.querySelector(".todo-list");
        if (e) {
            e.querySelectorAll("[data-todo-offcanvas-toogle]").forEach((t => {
                const a = o(t, "todo-offcanvas-target"),
                    n = e.querySelector(`#${a}`),
                    c = new window.bootstrap.Offcanvas(n, {
                        backdrop: !0
                    });
                t.addEventListener("click", (() => {
                    c.show();
                }));
            }));
        }
    };

    const tooltipInit = () => {
        [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')).map((t => new bootstrap.Tooltip(t, {
            trigger: "hover"
        })));
    };

    const mapboxInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, o = document.querySelectorAll(".mapbox-container");
        o && o.forEach((o => {
            window.mapboxgl.accessToken = "pk.eyJ1IjoidGhlbWV3YWdvbiIsImEiOiJjbGhmNW5ybzkxcmoxM2RvN2RmbW1nZW90In0.hGIvQ890TYkZ948MVrsMIQ";
            const t = o.querySelector("[data-mapbox]");
            if (t) {
                const o = e(t, "mapbox"),
                    n = document.querySelector(".zoomIn"),
                    a = document.querySelector(".zoomOut"),
                    c = document.querySelector(".fullScreen"),
                    r = {
                        default: "mapbox://styles/mapbox/light-v11",
                        light: "mapbox://styles/themewagon/clj57pads001701qo25756jtw",
                        dark: "mapbox://styles/themewagon/cljzg9juf007x01pk1bepfgew"
                    },
                    l = new window.mapboxgl.Map({
                        ...o,
                        container: "mapbox",
                        style: r[window.config.config.phoenixTheme]
                    });
                o.center && new window.mapboxgl.Marker({
                    color: getColor("primary")
                }).setLngLat(o.center).addTo(l), n && a && (n.addEventListener("click", (() => l.zoomIn())), a.addEventListener("click", (() => l.zoomOut()))), c && c.addEventListener("click", (() => l.getContainer().requestFullscreen()));
            }
        }));
    };

    const wizardInit = () => {
        const {
            getData: e
        } = window.phoenix.utils, t = "[data-theme-wizard]", a = "[data-wizard-step]", r = "[data-wizard-form]", d = "[data-wizard-password]", s = "[data-wizard-confirm-password]", o = "[data-wizard-next-btn]", l = "[data-wizard-prev-btn]", n = "[data-wizard-footer]", i = "submit", c = "show.bs.tab", u = "shown.bs.tab", m = "click";
        document.querySelectorAll(t).forEach((t => {
            const w = t.querySelectorAll(a),
                b = t.querySelectorAll(r),
                h = t.querySelector(d),
                p = t.querySelector(s),
                v = t.querySelector(o),
                f = t.querySelector(l),
                L = t.querySelector(n),
                y = new Event(i, {
                    bubbles: !0,
                    cancelable: !0
                }),
                z = t.hasAttribute("data-wizard-modal-disabled"),
                g = Array.from(w).map((e => window.bootstrap.Tab.getOrCreateInstance(e)));
            let E = 0,
                q = null;
            b.forEach((e => {
                e.addEventListener(i, (t => (t.preventDefault(), e.classList.contains("needs-validation") && (h && p && (h.value !== p.value ? p.setCustomValidity("Invalid field.") : p.setCustomValidity("")), !e.checkValidity()) ? (q.preventDefault(), !1) : (E += 1, null))));
            })), v.addEventListener(m, (() => {
                E + 1 < g.length && g[E + 1].show();
            })), f.addEventListener(m, (() => {
                E -= 1, g[E].show();
            })), w.length && w.forEach(((t, a) => {
                t.addEventListener(c, (a => {
                    const r = e(t, "wizard-step");
                    q = a, r > E && b[E].dispatchEvent(y);
                })), t.addEventListener(u, (() => {
                    E = a, E !== w.length - 1 || z || w.forEach((e => {
                        e.setAttribute("data-bs-toggle", "modal"), e.setAttribute("data-bs-target", "#error-modal");
                    }));
                    for (let e = 0; e < E; e += 1) w[e].classList.add("done"), e > 0 && w[e - 1].classList.add("complete");
                    for (let e = E; e < w.length; e += 1) w[e].classList.remove("done"), e > 0 && w[e - 1].classList.remove("complete");
                    E > w.length - 2 ? L.classList.add("d-none") : L.classList.remove("d-none"), E > 0 && E !== w.length - 1 ? f.classList.remove("d-none") : f.classList.add("d-none"), mapboxInit();
                }));
            }));
        }));
    };

    const faqTabInit = () => {
        const t = document.querySelectorAll("[data-vertical-category-tab]"),
            a = document.querySelector("[data-vertical-category-offcanvas]"),
            e = document.querySelectorAll("[data-category-filter]"),
            c = document.querySelectorAll(".faq-subcategory-tab .nav-item");
        if (a) {
            const e = window.bootstrap.Offcanvas ? .getOrCreateInstance(a);
            t.forEach((t => {
                t.addEventListener("click", (() => {
                    e.hide();
                }));
            }));
        }
        e && e.forEach((t => {
            t.classList.contains("active") && c.forEach((a => {
                a.classList.contains(t.getAttribute("data-category-filter")) || "all" === t.getAttribute("data-category-filter") || a.classList.add("d-none");
            })), t.addEventListener("click", (() => {
                c.forEach((a => {
                    "all" === t.getAttribute("data-category-filter") ? a.classList.remove("d-none") : a.classList.contains(t.getAttribute("data-category-filter")) || a.classList.add("d-none");
                }));
            }));
        }));
    };

    const kanbanInit = () => {
        const t = document.querySelector("[data-kanban-container]");
        if (t) {
            t.addEventListener("click", (t => {
                t.target.hasAttribute("data-kanban-collapse") && t.target.closest(".kanban-column").classList.toggle("collapsed");
            }));
            t.querySelectorAll("[data-sortable]").forEach((t => {
                window.Sortable.get(t).option("onStart", (t => {
                    document.body.classList.add("sortable-dragging"), window.Sortable.ghost.querySelector(".dropdown-menu").classList.remove("show");
                    const e = t.item.querySelector("[data-bs-toggle='dropdown']");
                    window.bootstrap.Dropdown.getInstance(e) ? .hide();
                }));
            }));
        }
    };

    const towFAVerificarionInit = () => {
        const t = document.querySelector("[data-2FA-varification]"),
            e = document.querySelectorAll("[data-2FA-varification] input[type=number]");
        if (t) {
            window.addEventListener("load", (() => e[0].focus())), t.addEventListener("keypress", (t => {
                t.target.matches("input[type=number]") && (/\D/.test(t.key) || t.target.value) && t.preventDefault();
            }));
            const a = [...e];
            t.addEventListener("input", (t => {
                if (t.target.matches("input[type=number]")) {
                    const e = a.indexOf(t.target),
                        i = a[e + 1];
                    i && "" !== t.target.value && i.hasAttribute("disabled") && (i.removeAttribute("disabled"), i.focus());
                }
            })), t.addEventListener("keydown", (t => {
                if (t.target.matches("input[type=number]") && 8 === t.keyCode) {
                    const e = a.indexOf(t.target),
                        i = a[e - 1];
                    i && (i.focus(), t.target.value = "", t.target.setAttribute("disabled", !0));
                }
            })), t.addEventListener("submit", (() => a.map((t => t.value)).join("")));
        }
    };

    const flightMapInit = () => {
            if (document.querySelector("#flightMap")) {
                window.mapboxgl.accessToken = "pk.eyJ1IjoidGhlbWV3YWdvbiIsImEiOiJjbGhmNW5ybzkxcmoxM2RvN2RmbW1nZW90In0.hGIvQ890TYkZ948MVrsMIQ";
                const e = document.querySelector(".zoomIn"),
                    t = document.querySelector(".zoomOut"),
                    o = document.querySelector(".fullScreen"),
                    r = {
                        default: "mapbox://styles/mapbox/light-v11",
                        light: "mapbox://styles/themewagon/clj57pads001701qo25756jtw",
                        dark: "mapbox://styles/themewagon/cljzg9juf007x01pk1bepfgew"
                    },
                    n = new window.mapboxgl.Map({
                        container: "flightMap",
                        style: r[window.config.config.phoenixTheme],
                        center: [-73.102712, 7.102257],
                        zoom: 5,
                        pitch: 40,
                        attributionControl: !1
                    });
                e.addEventListener("click", (() => n.zoomIn())), t.addEventListener("click", (() => n.zoomOut())), o.addEventListener("click", (() => n.getContainer().requestFullscreen()));
                const a = [-61.100583, 5.044713],
                    i = [-74.2139449434892, 8.136553550752552],
                    l = [-84.913785, 10.325774],
                    s = {
                        type: "FeatureCollection",
                        features: [{
                            type: "Feature",
                            geometry: {
                                type: "LineString",
                                coordinates: [a, i]
                            }
                        }]
                    },
                    c = {
                        type: "FeatureCollection",
                        features: [{
                            type: "Feature",
                            geometry: {
                                type: "LineString",
                                coordinates: [i, l]
                            }
                        }]
                    };
                let d = 1;
                ({
                    type: "FeatureCollection",
                    features: [{
                        type: "Feature",
                        properties: {},
                        geometry: {
                            type: "Point",
                            coordinates: a
                        }
                    }, {
                        type: "Feature",
                        properties: {},
                        geometry: {
                            type: "Point",
                            coordinates: i
                        }
                    }, {
                        type: "Feature",
                        properties: {},
                        geometry: {
                            type: "Point",
                            coordinates: l
                        }
                    }]
                }).features.forEach((e => {
                    const t = document.createElement("div");
                    t.className = `marker-${d}`, new window.mapboxgl.Marker(t).setLngLat(e.geometry.coordinates).addTo(n), d += 1;
                }));
                const u = window.turf.length(s.features[0]),
                    p = window.turf.length(s.features[0]),
                    m = [],
                    g = [],
                    y = 500;
                for (let e = 0; e < u; e += u / y) {
                    const t = window.turf.along(s.features[0], e);
                    m.push(t.geometry.coordinates);
                }
                for (let e = 0; e < p; e += p / y) {
                    const t = window.turf.along(c.features[0], e);
                    g.push(t.geometry.coordinates);
                }
                s.features[0].geometry.coordinates = m, c.features[0].geometry.coordinates = g, n.on("load", (() => {
                    n.addSource("route", {
                        type: "geojson",
                        data: s.features[0]
                    }), n.addSource("route2", {
                        type: "geojson",
                        data: c.features[0]
                    }), n.addLayer({
                        id: "route",
                        source: "route",
                        type: "line",
                        paint: {
                            "line-width": 2,
                            "line-color": "dark" === getItemFromStore("phoenixTheme") ? getColor("primary") : getColor("primary-light")
                        }
                    }), n.addLayer({
                        id: "route2",
                        source: "route2",
                        type: "line",
                        paint: {
                            "line-width": 1,
                            "line-color": getColor("warning")
                        }
                    });
                }));
            }
        },
        themeController = document.body;
    themeController && themeController.addEventListener("clickControl", (() => {
        flightMapInit();
    }));

    const typedTextInit = () => {
        const e = document.querySelectorAll(".typed-text");
        e.length && window.Typed && e.forEach((e => new window.Typed(e, {
            strings: getData(e, "typedText"),
            typeSpeed: 70,
            backSpeed: 70,
            loop: !0,
            backDelay: 1e3
        })));
    };

    const priceTierFormInit = () => {
        const e = document.querySelectorAll(".price-tier-form");
        e && e.forEach((e => {
            const t = e.querySelector("[data-price-toggle]"),
                r = e.querySelectorAll("[data-pricing]"),
                c = e.querySelector("[data-pricing-collapse]"),
                a = new window.bootstrap.Collapse(c, {
                    toggle: !1
                });
            t.addEventListener("change", (t => {
                r[0].checked = !0, t.target.checked ? e.classList.add("active") : (e.classList.remove("active"), a.hide());
            })), r.forEach((e => {
                e.addEventListener("change", (e => {
                    "paid" === e.target.value ? a.show() : a.hide();
                }));
            }));
        }));
    };

    const nouisliderInit = () => {
        const {
            getData: i
        } = window.phoenix.utils;
        if (window.noUiSlider) {
            document.querySelectorAll("[data-nouislider]").forEach((e => {
                const n = i(e, "nouislider"),
                    o = window._.merge({
                        start: [10],
                        connect: [!0, !1],
                        step: 1,
                        range: {
                            min: [0],
                            max: [100]
                        },
                        tooltips: !0
                    }, n);
                window.noUiSlider.create(e, {
                    ...o
                });
            }));
        }
    };

    window.initMap = initMap, docReady(detectorInit), docReady(simplebarInit), docReady(toastInit), docReady(tooltipInit), docReady(featherIconsInit), docReady(basicEchartsInit), docReady(bulkSelectInit), docReady(listInit), docReady(anchorJSInit), docReady(popoverInit), docReady(formValidationInit), docReady(docComponentInit), docReady(swiperInit), docReady(productDetailsInit), docReady(ratingInit), docReady(quantityInit), docReady(dropzoneInit), docReady(choicesInit), docReady(tinymceInit), docReady(responsiveNavItemsInit), docReady(flatpickrInit), docReady(iconCopiedInit), docReady(isotopeInit), docReady(bigPictureInit), docReady(countupInit), docReady(phoenixOffcanvasInit), docReady(todoOffcanvasInit), docReady(wizardInit), docReady(reportsDetailsChartInit), docReady(glightboxInit), docReady(themeControl), docReady(searchInit), docReady(handleNavbarVerticalCollapsed), docReady(navbarInit), docReady(navbarComboInit), docReady(fullCalendarInit), docReady(picmoInit), docReady(chatInit), docReady(modalInit), docReady(lottieInit), docReady(navbarShadowOnScrollInit), docReady(dropdownOnHover), docReady(supportChatInit), docReady(sortableInit), docReady(copyLink), docReady(randomColorInit), docReady(faqTabInit), docReady(createBoardInit), docReady(advanceAjaxTableInit), docReady(kanbanInit), docReady(towFAVerificarionInit), docReady(mapboxInit), docReady(flightMapInit), docReady(typedTextInit), docReady(priceTierFormInit), docReady(nouisliderInit), docReady((() => {
        const t = document.querySelector("[data-selected-rows]"),
            o = document.getElementById("selectedRows");
        if (t) {
            const e = document.getElementById("bulk-select-example"),
                i = window.phoenix.BulkSelect.getInstance(e);
            t.addEventListener("click", (() => {
                o.innerHTML = JSON.stringify(i.getSelectedRows(), void 0, 2);
            }));
        }
    }));
    var phoenix = {
        utils: utils,
        BulkSelect: BulkSelect
    };

    return phoenix;

}));
//# sourceMappingURL=phoenix.js.map