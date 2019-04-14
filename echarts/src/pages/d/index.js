import $ from "jquery";
import React from "react";

import styles from './index.less'
import {
    G2,
    Chart,
    Geom,
    Axis,
    Tooltip,
    Coord,
    Label,
    Legend,
    View,
    Guide,
    Shape,
    Facet,
    Util
} from "bizcharts";
import DataSet from "@antv/data-set";

let data;
$.ajax({
    url: "/api/tagsc",
    async : false,
    success: (iData) => { data = iData.list }
});

export default class Jitter extends React.Component {
    render() {
        const data = [
            {
                month: "Jan",
                man: 7.0,
                women: 3.9
            },
            {
                month: "Feb",
                man: 6.9,
                women: 4.2
            },
            {
                month: "Mar",
                man: 9.5,
                women: 5.7
            },
            {
                month: "Apr",
                man: 14.5,
                women: 8.5
            },
            {
                month: "May",
                man: 18.4,
                women: 11.9
            },
            {
                month: "Jun",
                man: 21.5,
                women: 15.2
            },
            {
                month: "Jul",
                man: 25.2,
                women: 17.0
            },
            {
                month: "Aug",
                man: 26.5,
                women: 16.6
            },
            {
                month: "Sep",
                man: 23.3,
                women: 14.2
            },
            {
                month: "Oct",
                man: 18.3,
                women: 10.3
            },
            {
                month: "Nov",
                man: 13.9,
                women: 6.6
            },
            {
                month: "Dec",
                man: 9.6,
                women: 4.8
            }
        ];
        const ds = new DataSet();
        const dv = ds.createView().source(data);
        dv.transform({
            type: "fold",
            fields: ["man", "women"],
            // 展开字段集
            key: "city",
            // key字段
            value: "temperature" // value字段
        });
        const cols = {
            month: {
                range: [0, 1]
            }
        };
        return (
            <div className={styles.wrap}>
                <Chart height={400} data={dv} scale={cols} forceFit>
                    <Legend />
                    <Axis name="month" />
                    <Axis
                        name="temperature"
                        label={{
                            formatter: val => `${val}°C`
                        }}
                    />
                    <Tooltip
                        crosshairs={{
                            type: "y"
                        }}
                    />
                    <Geom
                        type="line"
                        position="month*temperature"
                        size={2}
                        color={"city"}
                        shape={"smooth"}
                    />
                    <Geom
                        type="point"
                        position="month*temperature"
                        size={4}
                        shape={"circle"}
                        color={"city"}
                        style={{
                            stroke: "#fff",
                            lineWidth: 1
                        }}
                    />
                </Chart>
            </div>
        );
    }
}
