import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Item from '@material-ui/core/Grid';
import { List, ListItem } from '@material-ui/core';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import Skill from './skill';
import WorkExperience from './work-experience';
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
        workExperience: {
            textTransform: 'uppercase',
            float: 'left'
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
        },
        skill: {
            borderRadius: '10px',
            backgroundColor: theme.palette.primary.main,
            float: 'left',
            padding: '3px 10px 3px 10px',
            margin: '3px 5px 3px 5px',
            color: 'white'
        },
        skillGroupTitle: {
            // fontStyle: 'italic',
            float: 'left',
            color: theme.palette.success.main,
        }
    }),
);

function GroupSkill({ name, group, classes }) {
    console.log(group)
    if (group) {
        return (
            <Grid item container spacing={1} direction='column'>
                <Grid item>
                    <Typography variant='h5' className={classes.skillGroupTitle}>{name}</Typography>
                </Grid>
                <Grid item container spacing={1} direction='row'>
                    {group.map(g => g.map(skill =>
                        <Skill skill={skill} />
                    ))
                    }
                </Grid>
            </Grid>
        )
    }
    return null
}
function ResumeBody({ resume }) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    const workExperiences = resume.workExperiences
    const frontendSkills = resume.skills.frontend
    const backendSkills = resume.skills.backend
    const devopsSkills = resume.skills.devops
    const cloudSkills = resume.skills.cloud


    return (

        <Grid container spacing={1} columns={{ sm: 3, md: 3, lg: 3 }} className={classes.work}>
            <Grid item xs={12} md={8} lg={8} container direction='column'>
                <Item>
                    <Typography variant="h3" className={classes.workExperience}>
                        Work Experience
                    </Typography>
                </Item>
                {workExperiences && workExperiences.map(work => {
                    return <Item><WorkExperience data={work} /></Item>
                })}
            </Grid>
            <Grid item xs={12} md={4} lg={4} container direction='column'>
                <Grid item>
                    <Typography variant="h3" className={classes.workExperience}>
                        Skills
                    </Typography>
                </Grid>
                <Grid item>
                    <GroupSkill name='Backend' group={backendSkills} classes={classes} />
                    <GroupSkill name='Frontend' group={frontendSkills} classes={classes} />
                    <GroupSkill name='Devops' group={devopsSkills} classes={classes} />
                    <GroupSkill name='Cloud' group={cloudSkills} classes={classes} />
                </Grid>
            </Grid>
        </Grid>
    );
}

export default ResumeBody;
