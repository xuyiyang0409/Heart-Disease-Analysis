import React, { Component } from 'react'
import Link from 'umi/link';
import styles from './style.less'

class Page extends Component{
	render(){
		return(
			<div className={styles.wrap}>
				<div className={styles.title}><h1>Heart Disease Analysis</h1><h3>Group：Master Branch</h3></div>
				<div className={styles.d_wrap}>
					<div className={styles.d1_wrap}>
						<Link to="/a"><h2>Graphs</h2></Link>
					</div>
					<div className={styles.d2_wrap}>
						<Link to="/predict"><h2>0-1 Prediction</h2></Link>
					</div>
					<div className={styles.d2_wrap}>
						<Link to="/predict2"><h2>Muti Prediction</h2></Link>
					</div>
				</div>

			</div>
		)
	}
}

export default Page