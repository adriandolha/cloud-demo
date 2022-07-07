import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import WorkExperience from './work-experience';
import Education from './education';
import { Fragment } from 'react';
import Skills from './skills';
import MarkedComponent from './marked-component';
const useStyles = makeStyles((theme) =>
    createStyles({
        root: {
            flexGrow: 1
        },
        jobTitle: {
            float: 'left'
        },
        company: {
            float: 'left'
        },
        sectionTitle: {
            fontWeight: 'bold',
            textTransform: 'uppercase',
            float: 'left',
            marginTop: theme.spacing(2),
        },
        work: {
            marginTop: '10px'
        },
        workDate: {
            fontStyle: 'italic',
            float: 'left',
            color: theme.palette.success.main,
        },
        tasks: {
            fontStyle: 'italic',
            float: 'left',
            color: theme.palette.success.main,
        },
        taskList: {
            listStyle: 'circle',
        }
    }),
);


function ResumeBody({ resume, onResize }) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    let workExperiences = resume.workExperiences

    return (
        <Grid item container spacing={4} columns={{ sm: 3, md: 3, lg: 3 }} className={classes.work}>
            <Grid item xs={6} md={6} lg={6} spacing={2} container direction='column'>
                <Grid item>
                    <MarkedComponent component={<Typography variant="h4" className={classes.sectionTitle}>
                        {resume.workExperienceTitle}
                    </Typography>} />

                </Grid>
                {workExperiences && workExperiences.map((work, i) => {
                    return (<Fragment key={i}>
                        <Grid item>
                            <WorkExperience resume={resume} data={work} onResize={onResize} />
                        </Grid>
                    </Fragment>)
                })}
                <Grid item>
                    <MarkedComponent component={<Typography variant="h4" className={classes.sectionTitle}>
                        {resume.educationTitle}
                    </Typography>} />
                </Grid>
                {resume.education && resume.education.map((data, i) => {
                    return <Fragment key={`edu-${i}`}><Grid item><Education data={data} /></Grid></Fragment>
                })}
            </Grid>
            <Grid item xs={6} md={6} lg={6}>
                <Skills resume={resume} />
            </Grid>
        </Grid>
    );
}

export default ResumeBody;
